"""Language declarations and the selected-language value."""

from dataclasses import dataclass
from typing import Generic, TypeVar

TranslationT = TypeVar("TranslationT")


@dataclass(frozen=True, slots=True)
class Language(Generic[TranslationT]):
    """One complete implementation of a translation contract."""

    locale: str
    name: str
    translations: TranslationT


@dataclass(frozen=True, slots=True)
class ResolvedLanguage(Generic[TranslationT]):
    """Language selected for one operation or request."""

    key: str
    locale: str
    translations: TranslationT
