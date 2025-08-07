from collections.abc import Generator

from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsFunction
from ee.zakk.external_permissions.perm_sync_types import FetchAllDocumentsIdsFunction
from ee.zakk.external_permissions.utils import generic_doc_sync
from zakk.access.models import DocExternalAccess
from zakk.configs.constants import DocumentSource
from zakk.connectors.teams.connector import TeamsConnector
from zakk.db.models import ConnectorCredentialPair
from zakk.indexing.indexing_heartbeat import IndexingHeartbeatInterface
from zakk.utils.logger import setup_logger

logger = setup_logger()


TEAMS_DOC_SYNC_LABEL = "teams_doc_sync"


def teams_doc_sync(
    cc_pair: ConnectorCredentialPair,
    fetch_all_existing_docs_fn: FetchAllDocumentsFunction,
    fetch_all_existing_docs_ids_fn: FetchAllDocumentsIdsFunction,
    callback: IndexingHeartbeatInterface | None,
) -> Generator[DocExternalAccess, None, None]:
    teams_connector = TeamsConnector(
        **cc_pair.connector.connector_specific_config,
    )
    teams_connector.load_credentials(cc_pair.credential.credential_json)

    yield from generic_doc_sync(
        cc_pair=cc_pair,
        fetch_all_existing_docs_ids_fn=fetch_all_existing_docs_ids_fn,
        callback=callback,
        doc_source=DocumentSource.TEAMS,
        slim_connector=teams_connector,
        label=TEAMS_DOC_SYNC_LABEL,
    )
