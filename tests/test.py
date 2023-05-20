from time import sleep
import pytest
from calculation.fibonacci import fibonacci_calc
from base.basepage import BasePage


@pytest.mark.parametrize("browser", ["CHROME", "FIREFOX", "EDGE"], indirect=True)
class TestExample():
    BP = BasePage()

    fibonacci = fibonacci_calc()
    balance = 0

    def test_SGRID(self, browser):
        browser.get('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
        assert browser.title, 'XYZ Bank'
        TestExample.BP.login(browser)
        TestExample.balance += TestExample.fibonacci
        TestExample.BP.remittance(browser, 'Deposited', TestExample.fibonacci, TestExample.balance)
        TestExample.balance -= TestExample.fibonacci
        TestExample.BP.remittance(browser, 'Withdrawn', TestExample.fibonacci, TestExample.balance)
        sleep(2)
        TestExample.BP.transactions(browser, browser.name)
