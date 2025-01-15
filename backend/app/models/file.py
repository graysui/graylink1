from typing import TypedDict

class FileInfo(TypedDict):
    name: str
    path: str
    type: str
    size: int
    modified: str
    extension: str 