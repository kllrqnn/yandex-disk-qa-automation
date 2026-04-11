import allure


class DiskAssertions:
    @staticmethod
    @allure.step("Проверка статус-кода {expected_code}")
    def assert_status_code(response, expected_code):
        assert (
            response.status_code == expected_code
        ), f"Ожидали {expected_code}, но получили {response.status_code}. Body: {response.text}"

    @staticmethod
    @allure.step("Проверка соответствия имени ресурса {expected_name}")
    def assert_resource_name(response, expected_name):
        json_data = response.json()
        assert (
            json_data.get("name") == expected_name
        ), f"Ожидали имя {expected_name}, но получили {json_data.get('name')}"

    @staticmethod
    @allure.step("Проверка типа ресурса {expected_type}")
    def assert_resource_type(response, expected_type):
        actual_type = response.json().get("type")
        assert (
            actual_type == expected_type
        ), f"Ожидали тип {expected_type}, но получили {actual_type}"

    @staticmethod
    @allure.step("Поиск ресурса {name} в списке")
    def find_item_and_assert(response, name):
        items = response.json().get("_embedded", {}).get("items", [])
        target = next((item for item in items if item["name"] == name), None)
        assert target is not None, f"Ресурс '{name}' не найден в списке!"
        return target

    @staticmethod
    @allure.step("Проверка успешного восстановления (201 или 202)")
    def assert_restore_success(response):
        assert response.status_code in [
            201,
            202,
        ], f"Ошибка восстановления! Статус: {response.status_code}, Ответ: {response.text}"
