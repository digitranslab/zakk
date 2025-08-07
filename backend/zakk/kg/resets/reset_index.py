from sqlalchemy.orm import Session

from zakk.db.document import reset_all_document_kg_stages
from zakk.db.models import Connector
from zakk.db.models import KGEntity
from zakk.db.models import KGEntityExtractionStaging
from zakk.db.models import KGEntityType
from zakk.db.models import KGRelationship
from zakk.db.models import KGRelationshipExtractionStaging
from zakk.db.models import KGRelationshipType
from zakk.db.models import KGRelationshipTypeExtractionStaging


def reset_full_kg_index__commit(db_session: Session) -> None:
    """
    Resets the knowledge graph index.
    """

    db_session.query(KGRelationship).delete()
    db_session.query(KGRelationshipType).delete()
    db_session.query(KGEntity).delete()
    db_session.query(KGRelationshipExtractionStaging).delete()
    db_session.query(KGEntityExtractionStaging).delete()
    db_session.query(KGRelationshipTypeExtractionStaging).delete()
    # Update all connectors to disable KG processing
    db_session.query(Connector).update({"kg_processing_enabled": False})

    # Only reset grounded entity types
    db_session.query(KGEntityType).filter(
        KGEntityType.grounded_source_name.isnot(None)
    ).update({"active": False})

    reset_all_document_kg_stages(db_session)

    db_session.commit()
