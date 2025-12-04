from pathlib import Path

try:
    from app.main import app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения web `app`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `app.main`.',
    )

try:
    from app.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
        'Проверьте и поправьте: они должны быть доступны в модуле '
        '`app.core.db`.',
    )


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

pytest_plugins = [
    'tests.fixtures.fixture_data',
]
