from app.crud.base import CRUDBase
from app.models.docs import Document
from app.schemas.mongodb.docs import DocumentCreate, DocumentUpdate
from app.exceptions import IsNotImplemented


class CRUDDocs(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    async def update(self, *args, **kwargs) -> Document: # noqa
        raise IsNotImplemented("CRUDDocs.update not implemented")


docs = CRUDDocs(Document)
