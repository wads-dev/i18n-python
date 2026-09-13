"""Language-agnostic catalog for a typed translation contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar, cast

from wads_dev.i18n.language import Language, ResolvedLanguage
from wads_dev.i18n.negotiation import negotiate_language
from wads_dev.i18n.resolver import Resolver

LanguageKeyT = TypeVar("LanguageKeyT", bound=str)
TranslationT = TypeVar("TranslationT")


class LanguageCatalog(Protocol[TranslationT]):
    def resolve(
        self, accept_language: str | None
    ) -> Resolver[TranslationT]: ...


@dataclass(frozen=True, slots=True)
class AvailableLangs(Generic[LanguageKeyT, TranslationT]):
    """Languages available for one typed translation contract."""

    languages: Mapping[LanguageKeyT, Language[TranslationT]]
    default: LanguageKeyT

    def resolve(self, accept_language: str | None) -> Resolver[TranslationT]:
        """Negotiate the request language and bind a resolver to its translations."""

        selected_key = negotiate_language(
            accept_language,
            locales={
                key: language.locale
                for key, language in self.languages.items()
            },
            default=self.default,
        )
        selected = self.languages[cast(LanguageKeyT, selected_key)]
        return Resolver(
            ResolvedLanguage(
                key=selected_key,
                locale=selected.locale,
                translations=selected.translations,
            )
        )
