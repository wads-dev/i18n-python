# @wads.dev/i18n-py

Framework-independent Python foundations for strongly typed internationalization.

`i18n-py` gives Python projects typed translation contracts, deferred string and message references, RFC-compliant `Accept-Language` negotiation and request-scoped resolvers. It has zero runtime dependencies and no framework lock-in.

> ⚠️ **Status: `0.0.1-alpha`**. Esta versão é um pré-lançamento alfa experimental (*super-alpha*). Contratos públicos, nomes de classes e métodos ainda sofrerão alterações antes da versão estável `1.0.0`.

---

## Wads.dev i18n ecosystem

| Package | Environment | Responsibility |
| --- | --- | --- |
| [`@wads.dev/i18n-ts`](https://github.com/wads-dev/i18n-ts) | TypeScript / JS | Core typed contracts, language loading, project configuration and portable JSON bundles. |
| [`@wads.dev/i18n-py`](https://github.com/wads-dev/i18n-py) | Python 3.11+ | Typed contracts, deferred references, `Accept-Language` negotiation and resolvers. |
| [`@wads.dev/i18n-react`](https://github.com/wads-dev/i18n-react) | React | Provider, hooks and rich translation rendering built on `i18n-ts`. |
| [`@wads.dev/i18n-html`](https://github.com/wads-dev/i18n-html) | DOM / Static | HTML bindings and static usage discovery built on `i18n-ts`. |
| [`@wads.dev/i18n-editor`](https://github.com/wads-dev/i18n-editor) | Tooling | Local web editor for inspecting and editing translation bundles. |

---

## Why it exists

Translation files are application code: their structure changes, keys move, languages grow, and mistakes should fail during type checking or static analysis rather than reach users in production.

- **Zero dependencies:** pure Python (3.11+), no external libraries required.
- **Typed structural contracts:** define an immutable dataclass or protocol per module. If a language misses a key or changes an argument signature, `mypy` or `pyright` detects it immediately.
- **Deferred references (`Text` and `Message`):** domain logic can refer to a translation without knowing which language will be resolved at runtime.
- **HTTP-independent negotiation:** parses standard RFC `Accept-Language` headers with quality weights (`q=`), wildcard matching (`*`), prefix fallbacks (`pt-BR` ➔ `pt`), with no coupling to FastAPI, Django, Flask, or any web framework.
- **PEP 561 compatible:** includes `py.typed` out of the box.

---

## Installation

### Via PyPI (após publicação)
```bash
pip install wads-dev-i18n
# ou com uv:
uv add wads-dev-i18n
```

### Via Git Tag (Alpha)
```bash
pip install git+https://github.com/wads-dev/i18n-py.git@v0.0.1-alpha
```

---

## Quickstart

### 1. Definir o contrato do módulo (`base.py`)

```python
from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True, slots=True)
class AppTranslation:
    welcome: str
    greet_user: Callable[[str], str]
```

### 2. Implementar os idiomas

```python
# en.py
en = AppTranslation(
    welcome="Welcome",
    greet_user=lambda name: f"Hello, {name}!",
)

# pt.py
pt = AppTranslation(
    welcome="Bem-vindo",
    greet_user=lambda name: f"Olá, {name}!",
)
```

### 3. Criar referências tipadas e catálogo

```python
from wads_dev.i18n import AvailableLangs, Language, Text, Message

WELCOME_TEXT = Text[AppTranslation](lambda lang: lang.welcome)
GREET_MESSAGE = Message[AppTranslation, [str]](lambda lang: lang.greet_user)

CATALOG = AvailableLangs(
    languages={
        "en": Language(locale="en-US", translations=en),
        "pt": Language(locale="pt-BR", translations=pt),
    },
    default="en",
)
```

### 4. Resolver a requisição

```python
# Negocia o Accept-Language e vincula ao idioma adequado
resolver = CATALOG.resolve("pt-BR,pt;q=0.9,en;q=0.8")

print(resolver.text(WELCOME_TEXT))       # "Bem-vindo"
print(resolver.message(GREET_MESSAGE, "Victor")) # "Olá, Victor!"
```

---

## License

MIT © [Wads.dev](https://github.com/wads-dev)
