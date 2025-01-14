from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class FileOperation(str, Enum):
    COPY = 'copy'
    MOVE = 'move'
    DELETE = 'delete'

class BatchOperationRequest(BaseModel):
    operation: FileOperation
    paths: List[str]
    target_path: Optional[str] = None

class FileInfo(BaseModel):
    name: str
    path: str
    type: str
    size: Optional[int] = None
    modified: Optional[str] = None
    extension: Optional[str] = None 