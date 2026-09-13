from collections.abc import Callable
from dataclasses import dataclass

from wads_dev.i18n import (
    AvailableLangs,
    Language,
    Message,
    Text,
    negotiate_language,
    parse_accept_language,
)


@dataclass(frozen=True, slots=True)
class SampleTranslation:
    greeting: str
    farewell: Callable[[str], str]
    calc: Callable[[int, int], str]


def test_parse_accept_language_quality_weights() -> None:
    header = "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7;foo=bar"
    preferences = parse_accept_language(header)

    assert [p.tag for p in preferences] == ["en-us", "en", "pt-br", "pt"]
    assert [p.quality for p in preferences] == [1.0, 0.9, 0.8, 0.7]


def test_parse_accept_language_empty_and_none() -> None:
    assert parse_accept_language(None) == ()
    assert parse_accept_language("") == ()
    assert parse_accept_language("   ") == ()
    assert parse_accept_language(",,,") == ()


def test_negotiate_language_scenarios() -> None:
    locales = {"en": "en-US", "pt": "pt-BR", "es": "es-ES"}

    # Exact locale match
    assert negotiate_language("pt-BR", locales=locales, default="en") == "pt"

    # Exact key match
    assert negotiate_language("es", locales=locales, default="en") == "es"

    # Base language prefix match (pt-PT matches pt-BR base)
    assert negotiate_language("pt-PT", locales=locales, default="en") == "pt"

    # Quality ordering: higher quality preference wins
    assert negotiate_language("es;q=0.5,pt-BR;q=0.9", locales=locales, default="en") == "pt"

    # Quality zero is ignored
    assert negotiate_language("pt-BR;q=0,es;q=0.5", locales=locales, default="en") == "es"

    # Wildcard matches default
    assert negotiate_language("*", locales=locales, default="pt") == "pt"

    # No match falls back to default
    assert negotiate_language("ja-JP,de-DE", locales=locales, default="en") == "en"


def test_available_langs_and_typed_references() -> None:
    en = SampleTranslation(
        greeting="Hello",
        farewell=lambda name: f"Goodbye, {name}!",
        calc=lambda a, b: f"Sum: {a + b}",
    )
    pt = SampleTranslation(
        greeting="Olá",
        farewell=lambda name: f"Tchau, {name}!",
        calc=lambda a, b: f"Soma: {a + b}",
    )

    catalog = AvailableLangs(
        languages={
            "en": Language(locale="en-US", name="English", translations=en),
            "pt": Language(locale="pt-BR", name="Português", translations=pt),
        },
        default="en",
    )

    GREETING = Text[SampleTranslation](lambda lang: lang.greeting)
    FAREWELL = Message[SampleTranslation, [str]](lambda lang: lang.farewell)
    CALC = Message[SampleTranslation, [int, int]](lambda lang: lang.calc)

    # Resolution with Portuguese preference
    pt_resolver = catalog.resolve("pt-BR,pt;q=0.9,en;q=0.5")
    assert pt_resolver.language.key == "pt"
    assert pt_resolver.language.locale == "pt-BR"
    assert pt_resolver.text(GREETING) == "Olá"
    assert pt_resolver.message(FAREWELL, "Victor") == "Tchau, Victor!"
    assert pt_resolver.message(CALC, 2, 3) == "Soma: 5"

    # Resolution with fallback to default
    default_resolver = catalog.resolve("fr-FR,de;q=0.8")
    assert default_resolver.language.key == "en"
    assert default_resolver.language.locale == "en-US"
    assert default_resolver.text(GREETING) == "Hello"
    assert default_resolver.message(FAREWELL, "Victor") == "Goodbye, Victor!"
    assert default_resolver.message(CALC, 10, 20) == "Sum: 30"
