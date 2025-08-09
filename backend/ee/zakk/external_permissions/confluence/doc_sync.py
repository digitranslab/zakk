"""
Rules defined here:
https://confluence.atlassian.com/conf85/check-who-can-view-a-page-1283360557.html
"""

from collections.abc import Generator

from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsFunction
from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsIdsFunction
from ee.zakk.external_permissions.utils import generic_doc_sync
from zakk.access.models import DocExternalAccess
from zakk.configs.constants import DocumentSource
from zakk.connectors.confluence.connector import ConfluenceConnector
from zakk.connectors.credentials_provider import ZakkDBCredentialsProvider
from zakk.db.models import ConnectorCredentialPair
from zakk.indexing.indexing_heartbeat import IndexingHeartbeatInterface
from zakk.utils.logger import setup_logger
from shared_configs.contextvars import get_current_tenant_id

logger = setup_logger()


CONFLUENCE_DOC_SYNC_LABEL = "confluence_doc_sync"


def confluence_doc_sync(
    cc_pair: ConnectorCredentialPair,
    fetch_all_existing_docs_fn: FetchAllDocumentsFunction,
    fetch_all_existing_docs_ids_fn: FetchAllDocumentsIdsFunction,
    callback: IndexingHeartbeatInterface | None,
) -> Generator[DocExternalAccess, None, None]:
    """
    Fetches document permissions from Confluence and yields DocExternalAccess objects.
    Compares fetched documents against existing documents in the DB for the connector.
    If a document exists in the DB but not in the Confluence fetch, it's marked as restricted.
    """
    confluence_connector = ConfluenceConnector(
        **cc_pair.connector.connector_specific_config
    )

    provider = ZakkDBCredentialsProvider(
        get_current_tenant_id(), "confluence", cc_pair.credential_id
    )
    confluence_connector.set_credentials_provider(provider)

    yield from generic_doc_sync(
        cc_pair=cc_pair,
        fetch_all_existing_docs_ids_fn=fetch_all_existing_docs_ids_fn,
        callback=callback,
        doc_source=DocumentSource.CONFLUENCE,
        slim_connector=confluence_connector,
        label=CONFLUENCE_DOC_SYNC_LABEL,
    )
