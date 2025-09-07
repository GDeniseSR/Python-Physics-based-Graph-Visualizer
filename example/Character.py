from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from collections.abc import Sequence

@dataclass
@total_ordering
class Character:
    name : str
    house : Sequence[str] | str = tuple()
    nickname : str = ""
    
    actor : str = ""
    
    kingsguard : bool = False
    royal : bool = False
    
    allies : Sequence[str] = tuple()
    
    parents : Sequence[str] = tuple()
    parentOf : Sequence[str] = tuple()
    siblings : Sequence[str] = tuple()
    marriedEngaged : Sequence[str] = tuple()
    
    killed : Sequence[str] = tuple()
    killedBy : Sequence[str] = tuple()
    
    serves : Sequence[str] = tuple()
    servedBy : Sequence[str] = tuple()
    
    guardianOf : Sequence[str] = tuple()
    guardedBy : Sequence[str] = tuple()
    
    abducted : Sequence[str] = tuple()
    abductedBy : Sequence[str] = tuple()
    
    def __eq__(self, other : Character | str) -> bool:
        if other == None:
            return self is None
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name
    
    def __lt__(self, other : Character | str) -> bool:
        if other == None:
            return self is None
        if isinstance(other, str):
            return self.name < other
        return self.name < other.name
    
    def __str__(self) -> str:
        return self.name