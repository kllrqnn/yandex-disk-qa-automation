import allure
import requests

from clients import BaseClient
from tools import Routes


class DiskResourcesClient(BaseClient):
    @allure.step("Получение информации о ресурсе: {path}")
    def get_resource_info(self, path: str):
        """GET запрос для получения метаданных

        Args:
            path (str): Путь к ресурсу в диске

        Returns:
            requests.Response: Обьект ответа от API
        """
        return self._request("GET", Routes.RESOURCES, params={"path": path})

    @allure.step("Создание папки: {path}")
    def create_folder(self, path: str):
        """Создание новой папки по указанному пути.

        Args:
            path (str): Путь создаваемой папки

        Returns:
            requests.Response: Обьект ответа от API
        """
        return self._request("PUT", Routes.RESOURCES, params={"path": path})

    @allure.step("Удаление ресурса: {path}")
    def delete_resource(self, path: str, permanently: bool = False):
        """Удаление ресурса

        Args:
            path (str): Путь к удаляемому ресурсу
            permanently (bool, optional): Если True, ресурс удалится безвозвратно,
                                        иначе - попадет в корзину.
                                        Defaults to False.

        Returns:
            requests.Response: Обьект ответа от API
        """
        params = {"path": path, "permanently": str(permanently).lower()}
        return self._request("DELETE", Routes.RESOURCES, params=params)

    @allure.step("Копирование: {from_path} -> {to_path}")
    def copy_resource(self, from_path: str, to_path: str):
        """Копирование файла или папки

        Args:
            from_path (str): Путь к источнику копирования
            to_path (str): Путь к месту назначения копии

        Returns:
            requests.Response: Обьект ответа от API
        """
        params = {"from": from_path, "path": to_path}
        return self._request("POST", f"{Routes.RESOURCES}/copy", params=params)

    @allure.step("Запрос ссылки для последующей загрузки файла в {path} Диска")
    def get_upload_link(self, path: str):
        """Запрос ссылки для последующей загрузки файла в диск

        Args:
            path (str): Путь в диске, куда будет загружен файл

        Returns:
            requests.Response: Обьект ответа от API
        """
        return self._request(
            "GET", Routes.UPLOAD, params={"path": path, "overwrite": "true"}
        )

    @allure.step("Загрузка файла по прямой ссылке")
    def upload_file_to_url(self, upload_url: str, local_path: str):
        """Загружает локальный файл на сервер по предоставленной прямой ссылке

        Args:
            upload_url (str): Прямая ссылка для загрузки файла
            local_path (str): Путь к локальному файлу в проекте

        Returns:
            Response: Обьект ответа от сервера
        """
        with open(local_path, "rb") as f:
            return requests.put(upload_url, data=f)
