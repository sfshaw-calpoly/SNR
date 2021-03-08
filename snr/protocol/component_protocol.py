from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class ComponentProtocol(Protocol):
    name: str

    def start(self) -> None:
        ...

    def join(self) -> None:
        ...
