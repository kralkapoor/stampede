# Stampede - CLAUDE.md

## Project Overview
Image processing toolkit for the Stampede business. Automates resizing, recolouring, masking, and AI avatar generation for rubber stamp artwork.

## Commands
- **Run app:** `uv run python main.pyw`
- **Run tests:** `uv run pytest`
- **Install deps:** `uv sync`
- **Install all (inc. dev):** `uv sync --all-groups`
- **Build exe:** `uv run pyinstaller --onedir --windowed --add-data "assets;assets" main.pyw`

## Architecture

### Entry Point
`main.pyw` - Launches PySide6 QApplication with `MainWindow`.

### Key Patterns
- **Mediator:** `gui/main_window.py` coordinates between dialogs and handlers. Handlers have no knowledge of GUI; dialogs have no knowledge of handlers.
- **Template Method:** `BaseImageHandler.execute()` defines the processing flow; subclasses implement `_handler_function()`.
- **Multiprocessing:** `BaseImageHandler` uses `Pool(4)` for batch image processing.

### Handler Hierarchy
```
BaseImageHandler (handling/base_image_handler.py)
├── CircleHandler (handling/imagehandler/)
├── RectangleHandler (handling/imagehandler/)
└── AvatarBaseHandler (handling/avatar_base_handler.py)
    ├── AvatarHandler (handling/avatar_handler.py)
    └── AvatarEditHandler (handling/avatar_edit_handler.py)
```

### Directory Layout
```
gui/              GUI layer (main_window.py + dialogs/)
handling/         Core processing logic and handlers
settings/         Config, constants, prompt templates
tests/            pytest suite with mocked fixtures
assets/           UI resources (logo, stickers)
img/              Working directory for input/output (gitignored)
```

### Config & Environment
- Static config in `settings/static_dicts.py` (colours, paths, valid formats)
- OpenAI credentials via `.env` file (loaded by `python-dotenv`)
- Avatar prompt template in `settings/avatar_prompt.py`

## Testing
- Framework: pytest
- `conftest.py` patches filesystem init globally (autouse fixture)
- Handler instances can be created without real filesystem
- OpenAI calls are mocked via `mock_openai_client` fixture

## Design Rules
- **Handlers must not import or reference GUI code.** Handlers are pure processing logic — they accept data, process it, and return results. They must never create dialogs, emit signals, or depend on PySide6.
- **Dialogs must not import or reference handler code.** Dialogs handle user interaction only — collecting input and displaying output.
- **MainWindow is the only bridge.** `gui/main_window.py` is the mediator that wires dialogs to handlers. All coupling between presentation and processing lives here and nowhere else.
- If a new handler or dialog is added, it must follow this separation. Never pass GUI widgets into handlers or processing logic into dialogs.

## Testing Conventions
- **BDD style:** All tests use GIVEN/WHEN/THEN comments to describe preconditions, actions, and assertions.
- **Test classes group by method:** One `class Test<MethodName>` per method under test (e.g. `TestIsValidFileType`, `TestColourSub`).
- **Test naming:** `test_<behaviour_description>` in snake_case (e.g. `test_accepts_jpg`, `test_none_results_skipped`).
- **Fixtures over setup:** Use pytest fixtures from `conftest.py` for handler instances and mocks. The autouse `patch_handler_init` fixture patches filesystem calls globally.
- **Mock external boundaries only:** Patch OpenAI clients, filesystem calls, and OS operations. Do not mock internal handler methods unless necessary for isolation.

## Code Conventions
- Private methods: `_method_name()`
- Constants: `ALL_CAPS`
- Handlers suffixed `_handler.py`, base classes prefixed `base_`
- File I/O: input from `img/`, output to `img/Processed/{Type}/`, originals archived to `img/zArchive/`
