from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class KnowledgeType(str, Enum):
    TITLE = "title"
    PARAGRAPH = "paragraph"

    TABLE = "table"
    TABLE_CAPTION = "table_caption"

    FIGURE = "figure"
    FIGURE_CAPTION = "figure_caption"

    FORMULA = "formula"
    FORMULA_CAPTION = "formula_caption"

    HEADER = "header"
    FOOTER = "footer"

    LIST = "list"
    UNKNOWN = "unknown"


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Region(BaseModel):
    type: KnowledgeType
    confidence: float
    bbox: BoundingBox


class KnowledgeObject(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: KnowledgeType
    content: Any | None = None
    bbox: Optional[BoundingBox] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Page(BaseModel):
    page_number: int
    knowledge_objects: List[KnowledgeObject] = Field(default_factory=list)
    regions: List[Region] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    document_name: str
    document_type: str
    pages: List[Page] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

