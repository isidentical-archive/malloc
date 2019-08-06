# malloc
Malloc interface for python
## Examples
```py
from malloc import Memory

mem = Memory.from_malloc(1000)
mem.as_buffer()
mem.free()
del mem

with Memory.from_calloc(10, 100) as mem:
    mem.cast(etc)
```
