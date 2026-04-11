import pytest

from clients import DiskResourcesClient, TrashClient
from tools import DiskAssertions, DiskFaker

pytest_plugins = ["fixtures.settings"]


@pytest.fixture
def disk_client(settings):
    """Инициализирует клиент для работы с основными ресурсами яндекс диска

    Args:
        settings: Обьект настроек, передаваемый из плагина

    Returns:
        DiskResourcesClient: Экземпляр клиента для управления папками и файлами
    """
    return DiskResourcesClient(settings)


@pytest.fixture
def trash_client(settings):
    """Инициализирует клиент для работы с корзиной яндекс диска

    Args:
        settings: Обьект настроек

    Returns:
        TrashClient: Экземпляр клиента для восстановления и очистки ресурсов
    """
    return TrashClient(settings)


@pytest.fixture
def disk_faker():
    """Предоставляет инструмент для генерации случайных данных для тестов

    Returns:
       DiskFaker: Экземпляр класса для создания уникальных имен папок и файлов
    """
    return DiskFaker()


@pytest.fixture
def disk_assertions():
    """Предоставляет набор assertions для API Диска

    Returns:
        DiskAssertions: Экземпляр класса с методами валидации ответов сервера
    """
    return DiskAssertions()
