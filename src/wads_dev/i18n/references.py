"""Deferred, typed references into a module translation contract."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar

TranslationT = TypeVar("TranslationT")
ParametersT = ParamSpec("ParametersT")


@dataclass(frozen=True, slots=True)
class Text(Generic[TranslationT]):
    """Reference to a plain string inside a typed translation contract."""

    select: Callable[[TranslationT], str]


@dataclass(frozen=True, slots=True)
class Message(Generic[TranslationT, ParametersT]):
    """Reference to an interpolated function inside a typed translation contract."""

    select: Callable[[TranslationT], Callable[ParametersT, str]]
