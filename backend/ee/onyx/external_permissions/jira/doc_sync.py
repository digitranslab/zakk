from collections.abc import Generator

from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsFunction
from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsIdsFunction
from ee.zakk.external_permissions.utils import generic_doc_sync
from zakk.access.models import DocExternalAccess
from zakk.configs.constants import DocumentSource
from zakk.connectors.jira.connector import JiraConnector
from zakk.db.models import ConnectorCredentialPair
from zakk.indexing.indexing_heartbeat import IndexingHeartbeatInterface
from zakk.utils.logger import setup_logger

logger = setup_logger()

JIRA_DOC_SYNC_TAG = "jira_doc_sync"


def jira_doc_sync(
    cc_pair: ConnectorCredentialPair,
    fetch_all_existing_docs_fn: FetchAllDocumentsFunction,
    fetch_all_existing_docs_ids_fn: FetchAllDocumentsIdsFunction,
    callback: IndexingHeartbeatInterface | None = None,
) -> Generator[DocExternalAccess, None, None]:
    jira_connector = JiraConnector(
        **cc_pair.connector.connector_specific_config,
    )
    jira_connector.load_credentials(cc_pair.credential.credential_json)

    yield from generic_doc_sync(
        cc_pair=cc_pair,
        fetch_all_existing_docs_ids_fn=fetch_all_existing_docs_ids_fn,
        callback=callback,
        doc_source=DocumentSource.JIRA,
        slim_connector=jira_connector,
        label=JIRA_DOC_SYNC_TAG,
    )
