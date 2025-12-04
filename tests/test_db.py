from .conftest import BASE_DIR


try:
    from app.core.config import Settings
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект настроек приложения web `Settings`.'
        'Проверьте и поправьте: он должен быть доступен в модуле '
        '`web.core.config`.',
    )


def test_check_migration_file_exist():
    """
    Проверяет наличие папки `alembic` и файла миграций.
    """
    app_dirs = [d.name for d in BASE_DIR.iterdir()]
    assert 'alembic' in app_dirs, (
        'В корневой директории не обнаружена папка `alembic`.'
    )
    ALEMBIC_DIR = BASE_DIR / 'alembic'
    version_dir = [d.name for d in ALEMBIC_DIR.iterdir()]
    assert 'versions' in version_dir, (
        'В папке `alembic` не обнаружена папка `versions`'
    )
    VERSIONS_DIR = ALEMBIC_DIR / 'versions'
    files_in_version_dir = [
        f.name for f in VERSIONS_DIR.iterdir() if (
            f.is_file() and 'init' not in f.name
        )
    ]
    assert len(files_in_version_dir) > 0, (
        'В папке `alembic.versions` не обнаружены файлы миграций'
    )
