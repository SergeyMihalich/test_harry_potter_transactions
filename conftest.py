import pytest as pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture
def browser(request):
    browser_name = request.param
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=getattr(DesiredCapabilities, browser_name)
    )
    request.cls.driver = driver
    yield driver
    driver.quit()


@pytest.fixture(params=["CHROME", "FIREFOX", "EDGE"])
def browser_param(request):
    return request.param


# @pytest.fixture(scope='session')
# def browser():
#     # Инициализация драйвера Chrome
#     driver = webdriver.Chrome()
#     # Передача драйвера в тесты
#     yield driver
#
#     # Завершение работы драйвера после выполнения всех тестов
#     driver.quit()
