import csv
import io
from datetime import datetime

from celery import shared_task
from celery import Task

from ee.zakk.server.query_history.api import fetch_and_process_chat_session_history
from ee.zakk.server.query_history.api import ZAKK_ANONYMIZED_EMAIL
from ee.zakk.server.query_history.models import QuestionAnswerPairSnapshot
from zakk.background.celery.apps.heavy import celery_app
from zakk.background.task_utils import construct_query_history_report_name
from zakk.configs.app_configs import JOB_TIMEOUT
from zakk.configs.app_configs import ZAKK_QUERY_HISTORY_TYPE
from zakk.configs.constants import FileOrigin
from zakk.configs.constants import FileType
from zakk.configs.constants import ZakkCeleryTask
from zakk.configs.constants import QueryHistoryType
from zakk.db.engine.sql_engine import get_session_with_current_tenant
from zakk.db.tasks import delete_task_with_id
from zakk.db.tasks import mark_task_as_finished_with_id
from zakk.db.tasks import mark_task_as_started_with_id
from zakk.file_store.file_store import get_default_file_store
from zakk.utils.logger import setup_logger


logger = setup_logger()


@shared_task(
    name=ZakkCeleryTask.EXPORT_QUERY_HISTORY_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
    bind=True,
    trail=False,
)
def export_query_history_task(
    self: Task,
    *,
    start: datetime,
    end: datetime,
    start_time: datetime,
    # Need to include the tenant_id since the TenantAwareTask needs this
    tenant_id: str,
) -> None:
    if not self.request.id:
        raise RuntimeError("No task id defined for this task; cannot identify it")

    task_id = self.request.id
    stream = io.StringIO()
    writer = csv.DictWriter(
        stream,
        fieldnames=list(QuestionAnswerPairSnapshot.model_fields.keys()),
    )
    writer.writeheader()

    with get_session_with_current_tenant() as db_session:
        try:
            mark_task_as_started_with_id(
                db_session=db_session,
                task_id=task_id,
            )

            snapshot_generator = fetch_and_process_chat_session_history(
                db_session=db_session,
                start=start,
                end=end,
            )

            for snapshot in snapshot_generator:
                if ZAKK_QUERY_HISTORY_TYPE == QueryHistoryType.ANONYMIZED:
                    snapshot.user_email = ZAKK_ANONYMIZED_EMAIL

                writer.writerows(
                    qa_pair.to_json()
                    for qa_pair in QuestionAnswerPairSnapshot.from_chat_session_snapshot(
                        snapshot
                    )
                )

        except Exception:
            logger.exception(f"Failed to export query history with {task_id=}")
            mark_task_as_finished_with_id(
                db_session=db_session,
                task_id=task_id,
                success=False,
            )
            raise

    report_name = construct_query_history_report_name(task_id)
    with get_session_with_current_tenant() as db_session:
        try:
            stream.seek(0)
            get_default_file_store().save_file(
                content=stream,
                display_name=report_name,
                file_origin=FileOrigin.QUERY_HISTORY_CSV,
                file_type=FileType.CSV,
                file_metadata={
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "start_time": start_time.isoformat(),
                },
                file_id=report_name,
            )

            delete_task_with_id(
                db_session=db_session,
                task_id=task_id,
            )
        except Exception:
            logger.exception(
                f"Failed to save query history export file; {report_name=}"
            )
            mark_task_as_finished_with_id(
                db_session=db_session,
                task_id=task_id,
                success=False,
            )
            raise


celery_app.autodiscover_tasks(
    [
        "ee.zakk.background.celery.tasks.doc_permission_syncing",
        "ee.zakk.background.celery.tasks.external_group_syncing",
        "ee.zakk.background.celery.tasks.cleanup",
    ]
)
