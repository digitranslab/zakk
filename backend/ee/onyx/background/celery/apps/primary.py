from datetime import datetime
from datetime import timezone
from uuid import UUID

from celery import shared_task
from celery import Task

from ee.zakk.background.celery_utils import should_perform_chat_ttl_check
from ee.zakk.background.task_name_builders import name_chat_ttl_task
from ee.zakk.server.reporting.usage_export_generation import create_new_usage_report
from zakk.background.celery.apps.primary import celery_app
from zakk.configs.app_configs import JOB_TIMEOUT
from zakk.configs.constants import ZakkCeleryTask
from zakk.db.chat import delete_chat_session
from zakk.db.chat import get_chat_sessions_older_than
from zakk.db.engine.sql_engine import get_session_with_current_tenant
from zakk.db.enums import TaskStatus
from zakk.db.tasks import mark_task_as_finished_with_id
from zakk.db.tasks import register_task
from zakk.server.settings.store import load_settings
from zakk.utils.logger import setup_logger

logger = setup_logger()

# mark as EE for all tasks in this file


@shared_task(
    name=ZakkCeleryTask.PERFORM_TTL_MANAGEMENT_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
    bind=True,
    trail=False,
)
def perform_ttl_management_task(
    self: Task, retention_limit_days: int, *, tenant_id: str
) -> None:
    task_id = self.request.id
    if not task_id:
        raise RuntimeError("No task id defined for this task; cannot identify it")

    start_time = datetime.now(tz=timezone.utc)

    user_id: UUID | None = None
    session_id: UUID | None = None
    try:
        with get_session_with_current_tenant() as db_session:
            # we generally want to move off this, but keeping for now
            register_task(
                db_session=db_session,
                task_name=name_chat_ttl_task(retention_limit_days, tenant_id),
                task_id=task_id,
                status=TaskStatus.STARTED,
                start_time=start_time,
            )

            old_chat_sessions = get_chat_sessions_older_than(
                retention_limit_days, db_session
            )

        for user_id, session_id in old_chat_sessions:
            # one session per delete so that we don't blow up if a deletion fails.
            with get_session_with_current_tenant() as db_session:
                delete_chat_session(
                    user_id,
                    session_id,
                    db_session,
                    include_deleted=True,
                    hard_delete=True,
                )

        with get_session_with_current_tenant() as db_session:
            mark_task_as_finished_with_id(
                db_session=db_session,
                task_id=task_id,
                success=True,
            )

    except Exception:
        logger.exception(
            "delete_chat_session exceptioned. "
            f"user_id={user_id} session_id={session_id}"
        )
        with get_session_with_current_tenant() as db_session:
            mark_task_as_finished_with_id(
                db_session=db_session,
                task_id=task_id,
                success=False,
            )
        raise


#####
# Periodic Tasks
#####


@celery_app.task(
    name=ZakkCeleryTask.CHECK_TTL_MANAGEMENT_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
)
def check_ttl_management_task(*, tenant_id: str) -> None:
    """Runs periodically to check if any ttl tasks should be run and adds them
    to the queue"""

    settings = load_settings()
    retention_limit_days = settings.maximum_chat_retention_days
    with get_session_with_current_tenant() as db_session:
        if should_perform_chat_ttl_check(retention_limit_days, db_session):
            perform_ttl_management_task.apply_async(
                kwargs=dict(
                    retention_limit_days=retention_limit_days, tenant_id=tenant_id
                ),
            )


@celery_app.task(
    name=ZakkCeleryTask.AUTOGENERATE_USAGE_REPORT_TASK,
    ignore_result=True,
    soft_time_limit=JOB_TIMEOUT,
)
def autogenerate_usage_report_task(*, tenant_id: str) -> None:
    """This generates usage report under the /admin/generate-usage/report endpoint"""
    with get_session_with_current_tenant() as db_session:
        create_new_usage_report(
            db_session=db_session,
            user_id=None,
            period=None,
        )


celery_app.autodiscover_tasks(
    [
        "ee.zakk.background.celery.tasks.doc_permission_syncing",
        "ee.zakk.background.celery.tasks.external_group_syncing",
        "ee.zakk.background.celery.tasks.cloud",
    ]
)
