"""Resolution of deferred references against one selected language."""

from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar

from wads_dev.i18n.language import ResolvedLanguage
from wads_dev.i18n.references import Message, Text

TranslationT = TypeVar("TranslationT")
ParametersT = ParamSpec("ParametersT")


@dataclass(frozen=True, slots=True)
class Resolver(Generic[TranslationT]):
    """Resolve plain and interpolated references for one selected language."""

    language: ResolvedLanguage[TranslationT]

    def text(self, reference: Text[TranslationT]) -> str:
        return reference.select(self.language.translations)

    def message(
        self,
        reference: Message[TranslationT, ParametersT],
        *args: ParametersT.args,
        **kwargs: ParametersT.kwargs,
    ) -> str:
        interpolate = reference.select(self.language.translations)
        return interpolate(*args, **kwargs)
