"""HTTP-independent Accept-Language negotiation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LanguagePreference:
    tag: str
    quality: float
    position: int


def parse_accept_language(value: str | None) -> tuple[LanguagePreference, ...]:
    """Parse and order an Accept-Language value by quality and appearance."""

    preferences: list[LanguagePreference] = []
    for position, raw_item in enumerate((value or "").split(",")):
        item = raw_item.strip()
        if not item:
            continue
        raw_tag, *parameters = item.split(";")
        quality = 1.0
        for parameter in parameters:
            name, separator, raw_value = parameter.strip().partition("=")
            if separator and name.casefold() == "q":
                try:
                    quality = min(1.0, max(0.0, float(raw_value)))
                except ValueError:
                    quality = 0.0
        preferences.append(
            LanguagePreference(
                tag=raw_tag.strip().casefold().replace("_", "-"),
                quality=quality,
                position=position,
            )
        )
    return tuple(
        sorted(preferences, key=lambda item: (-item.quality, item.position))
    )


def negotiate_language(
    accept_language: str | None, *, locales: dict[str, str], default: str
) -> str:
    """Return a language key using exact, regional, then base-language matches."""

    normalized_locales = {
        key: locale.casefold().replace("_", "-")
        for key, locale in locales.items()
    }
    for preference in parse_accept_language(accept_language):
        if preference.quality == 0:
            continue
        if preference.tag == "*":
            return default
        requested_base = preference.tag.split("-", 1)[0]
        for key, locale in normalized_locales.items():
            if preference.tag == locale or preference.tag == key.casefold():
                return key
        for key, locale in normalized_locales.items():
            if requested_base == locale.split("-", 1)[0]:
                return key
    return default
