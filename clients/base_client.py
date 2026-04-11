import json

import allure
import requests

from tools import get_logger


class BaseClient:
    def __init__(self, settings):
        self.base_url = settings.base_url.strip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"OAuth {settings.yandex_disk_token}"}
        )
        self.logger = get_logger(self.__class__.__name__)

    def _request(self, method: str, route: str, **kwargs):
        """Базовый метод для отправки HTTP-запросов с логированием и аттачами в Allure

        Args:
            method (str): HTTP метод
            route (str): Ендпоинт

        Returns:
            requests.Response: Обьект ответа от сервера
        """
        url = f"{self.base_url}{route}"

        self.logger.info(f"Sending {method} request to {url}")
        if kwargs.get("params"):
            self.logger.debug(f"Params: {kwargs.get('params')}")

        allure_request_data = (
            f"Method: {method}\nURL: {url}\nParams: {kwargs.get('params')}"
        )
        allure.attach(
            allure_request_data,
            name="Request Details",
            attachment_type=allure.attachment_type.TEXT,
        )

        response = self.session.request(method, url, **kwargs)

        if not response.text:
            allure.attach(
                "Empty body",
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response

        try:
            response_body = json.dumps(response.json(), indent=4, ensure_ascii=False)
            allure.attach(
                response_body,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )
        except (json.JSONDecodeError, ValueError):
            allure.attach(
                response.text,
                name="Response Body (Raw)",
                attachment_type=allure.attachment_type.TEXT,
            )

        self.logger.info(f"Response status: {response.status_code}")
        return response
