"""
Base classes and types for llmcli
"""

from typing import Any, TypedDict

from rich.console import RenderableType
from rich.padding import Padding


class NoPadding(Padding):
    """
    Empty Renderable
    """

    def __init__(self, renderable: RenderableType, **kwargs: Any) -> None:
        """
        Create an empty Padding
        """
        _ = kwargs
        pad = (0, 0, 0, 0)
        super().__init__(renderable, pad=pad)


class Message(TypedDict):
    """
    Message
    """

    role: str
    content: str