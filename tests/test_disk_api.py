import allure


@allure.epic("Yandex Disk API")
@allure.feature("Resources Operations")
class TestYandexDiskAPI:

    @allure.story("Управление папками")
    @allure.title("Успешное создание и получение инфо о папке")
    def test_folder_creation_and_info(self, disk_client, disk_faker, disk_assertions):
        folder_name = disk_faker.random_folder_name()

        with allure.step("Создаем папку"):
            res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(res, 201)

        with allure.step("Проверяем метаданные"):
            info = disk_client.get_resource_info(folder_name)
            disk_assertions.assert_status_code(info, 200)
            disk_assertions.assert_resource_name(info, folder_name)
            disk_assertions.assert_resource_type(info, "dir")

    @allure.story("Управление папками")
    @allure.title("Успешное копирование папки")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_copy_folder(self, disk_client, disk_faker, disk_assertions):
        folder_name = disk_faker.random_folder_name()
        copy_name = f"{folder_name}_copy"

        with allure.step("Создаем исходную папку"):
            create_res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(create_res, 201)

        with allure.step("Копируем"):
            copy_res = disk_client.copy_resource(folder_name, copy_name)
            disk_assertions.assert_status_code(copy_res, 201)

        with allure.step("проверяем, что копия существует"):
            info_res = disk_client.get_resource_info(copy_name)
            disk_assertions.assert_status_code(info_res, 200)

    @allure.story("Корзина")
    @allure.title("Успешное удаление и восстановление")
    def test_delete_to_trash_and_restore(
        self, disk_client, trash_client, disk_faker, disk_assertions
    ):
        folder_name = disk_faker.random_folder_name()

        with allure.step("Cоздание и удаление"):
            create_res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(create_res, 201)
            disk_client.delete_resource(folder_name)

        with allure.step("Восстановление из корзины"):
            trash_res = trash_client.get_trash_resources()
            target = disk_assertions.find_item_and_assert(trash_res, folder_name)

            restore_res = trash_client.restore_resource(target["path"])
            assert restore_res.status_code in [201, 202]

        with allure.step("проверка: папка снова на месте"):
            info = disk_client.get_resource_info(folder_name)
            disk_assertions.assert_status_code(info, 200)

    @allure.story("Управление файлами")
    @allure.title("Полный цикл загрузки файла")
    def test_upload_file_flow(self, disk_client, disk_faker, disk_assertions):
        folder_name = disk_faker.random_folder_name()
        disk_path = f"{folder_name}/test.txt"

        with allure.step("Создание папки"):
            create_res = disk_client.create_folder(folder_name)
            disk_assertions.assert_status_code(create_res, 201)

        with allure.step("Загрузка файла"):
            link_res = disk_client.get_upload_link(disk_path)
            url = link_res.json().get("href")

            upload_res = disk_client.upload_file_to_url(url, "files/test_sample.txt")
            disk_assertions.assert_status_code(upload_res, 201)

        with allure.step("Проверка типа файла"):
            info = disk_client.get_resource_info(disk_path)
            disk_assertions.assert_resource_type(info, "file")
