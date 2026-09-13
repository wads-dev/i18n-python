"""Typed, framework-independent internationalization."""

from wads_dev.i18n.catalog import AvailableLangs, LanguageCatalog
from wads_dev.i18n.language import Language, ResolvedLanguage
from wads_dev.i18n.negotiation import (
    LanguagePreference,
    negotiate_language,
    parse_accept_language,
)
from wads_dev.i18n.references import Message, Text
from wads_dev.i18n.resolver import Resolver

__all__ = [
    "AvailableLangs",
    "Language",
    "LanguageCatalog",
    "LanguagePreference",
    "Message",
    "ResolvedLanguage",
    "Resolver",
    "Text",
    "negotiate_language",
    "parse_accept_language",
]
