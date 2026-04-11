import allure

from clients import BaseClient
from tools import Routes


class TrashClient(BaseClient):
    @allure.step("Получение списка ресурсов в корзине")
    def get_trash_resources(self, path=None):
        """Запрашивает содержимое корзины или информацию о конкретном ресурсе в ней

        Args:
            path (str, optional):Путь к ресурсу в корзине.
                                Если не указан, возвращается содержимое корня корзины.
                                Defaults to None.

        Returns:
            Response: Обьект ответа
        """
        params = {}
        if path:
            params["path"] = (
                path if path.startswith("trash:/") else f"trash:/{path.strip('/')}"
            )

        return self._request("GET", Routes.TRASH_RESOURCES, params=params)

    @allure.step("Восстановление ресурса из корзины: {path}")
    def restore_resource(self, path: str):
        """Восстанавливает ресурс из корзины в его исходную директорию

        Args:
            path (str): Путь к восстанавливаемому ресурсу

        Returns:
            Response: Обьект ответа
        """
        full_path = path if path.startswith("trash:/") else f"trash:/{path.strip('/')}"

        return self._request("PUT", Routes.TRASH_RESTORE, params={"path": full_path})

    @allure.step("Очистка корзины")
    def clear_trash(self, path: str = None):
        """Полностью очищает корзину или удаляет из нее конкретный ресурс

        Args:
            path (str, optional):Путь к конкретному ресурсу для окончательного удаления.
                                Если None, очищается вся корзина.
                                Defaults to None.

        Returns:
            Response: Обьект ответа
        """
        params = {"path": path} if path else {}
        return self._request("DELETE", Routes.TRASH_RESOURCES, params=params)
