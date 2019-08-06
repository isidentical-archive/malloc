from __future__ import annotations

import ctypes
from contextlib import AbstractContextManager
from dataclasses import dataclass
from enum import Enum, auto
from typing import TypeVar

T: ctypes._SimpleCData = TypeVar("T")
PADDING: int = 8

class State(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    FREED = auto()

@dataclass
class Memory(AbstractContextManager):
    size: int
    addr: int
    state: bool = State.ACTIVE

    def __post_init__(self):
        if self.addr < 0:
            self.state = State.INACTIVE

    def cast(self, typ: T) -> T:
        return ctypes.cast(self.addr, typ)
    
    def as_buffer(self) -> int:
        buf = self.cast(ctypes.c_char_p)
        obj = ctypes.pythonapi.PyBytes_FromString(buf)
        return obj

    @classmethod
    def from_malloc(cls, size: int) -> Memory:
        addr = ctypes.pythonapi.PyMem_Malloc(size)
        return cls(size, addr)

    @classmethod
    def from_calloc(cls, nelem: int, elsize: int) -> Memory:
        addr = ctypes.pythonapi.PyMem_Calloc(nelem, elsize)
        return cls(nelem * elsize + PADDING, addr)

    @classmethod
    def from_realloc(cls, other: Memory, size: int = None) -> Memory:
        size = size or other.size
        addr = ctypes.pythonapi.PyMem_Realloc(other.addr, size)
        return Memory(size, addr)
    
    def free(self) -> None:
        self.state = State.FREED
        ctypes.pythonapi.PyMem_Free(self.addr)
    
    def __exit__(self, *exc_info):
        self.free()

    __del__ = free
