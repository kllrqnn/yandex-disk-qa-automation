from copy import deepcopy

import allure

from clients import DiskResourcesClient


@allure.epic("Yandex Disk API")
@allure.feature("Negative and Security Scenarios")
class TestYandexDiskNegative:

    @allure.story("Негативные сценарии")
    @allure.title("Ошибка при создании уже существующей папки")
    def test_create_duplicate_folder(self, disk_client, disk_faker, disk_assertions):
        folder_name = disk_faker.random_folder_name()

        with allure.step("Создаем папку"):
            create_res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(create_res, 201)

        with allure.step("Повторное создание той же папки"):
            res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(res, 409)
            disk_assertions.assert_error_message(res, "уже существует")

    @allure.story("Негативные сценарии")
    @allure.title("Запрос инфо о несуществующем ресурсе")
    def test_get_info_non_existent(self, disk_client, disk_assertions):
        path = "non_existent_folder_12345"

        with allure.step(f"Запрашиваем информацию о несуществующем пути {path}"):
            res = disk_client.get_resource_info(path)
            disk_assertions.assert_status_code(res, 404)
            disk_assertions.assert_error_message(
                res, "Не удалось найти запрошенный ресурс."
            )

    @allure.story("Негативные сценарии")
    @allure.title("Удаление несуществующей папки")
    def test_delete_non_existent(self, disk_client, disk_assertions):
        path = "trash_me_but_i_dont_exist"

        with allure.step(f"Пытаемся удалить несуществующий ресурс {path}"):
            res = disk_client.delete_resource(path)
            disk_assertions.assert_status_code(res, 404)

    @allure.story("Авторизация")
    @allure.title("Запрос с невалидным токеном")
    def test_invalid_token(self, settings, disk_assertions):
        with allure.step("Подготовка клиента с невалидным токеном"):
            bad_settings = deepcopy(settings)
            bad_settings.yandex_disk_token = "INVALID_TOKEN_123"
            bad_client = DiskResourcesClient(bad_settings)

        with allure.step("Выполнение запроса под неавторизованным пользователем"):
            res = bad_client.get_resource_info("/")
            disk_assertions.assert_status_code(res, 401)
            disk_assertions.assert_error_message(res, "Не авторизован.")

    @allure.story("Граничные значения")
    @allure.title("Создание папки с очень длинным именем")
    def test_long_name_folder(self, disk_client, disk_assertions):
        long_name = "a" * 250

        with allure.step(f"Создаем папку с именем длиной {len(long_name)} символов"):
            res = disk_client.create_folder(long_name)
            disk_assertions.assert_status_code(res, 201)

        with allure.step("Очистка: удаление созданной длинной папки"):
            delete_res = disk_client.delete_resource(long_name, permanently=True)
            assert delete_res.status_code in [202, 204]

    @allure.story("Корзина")
    @allure.title("Очистка пустой корзины")
    def test_clear_empty_trash(self, trash_client, disk_assertions):
        with allure.step("Предварительная полная очистка"):
            res_first = trash_client.clear_trash()
            disk_assertions.assert_delete_success(res_first)

        with allure.step("Повторная очистка пустой корзины"):
            res_second = trash_client.clear_trash()
            disk_assertions.assert_delete_success(res_second)
