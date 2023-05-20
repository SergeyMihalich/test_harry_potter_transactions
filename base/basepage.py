import csv
from time import sleep
import re
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    def login(self, browser):
        batton_customer_login = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-primary[ng-click="customer()"]')))
        batton_customer_login.click()
        select_login = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.ID, 'userSelect')))
        select_login.send_keys('Harry Potter')
        select_login.click()
        click_login = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-default')))
        click_login.click()

    def remittance(self, browser, name, money, balance):
        battons = {
            'Deposited': 2,
            'Withdrawn': 3
        }
        select_remittance = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'[ng-class="btnClass{battons[name]}"]')))
        select_remittance.click()

        while True:
            check_loading = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.form-group label')))
            if check_loading.text == f'Amount to be {name} :':
                break
            sleep(1)

        enter_remittance = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.form-group label+input')))
        enter_remittance.click()
        enter_remittance.send_keys(money)

        remittance_click = \
            browser.find_element(By.CSS_SELECTOR, '.btn-default')
        remittance_click.click()

        balance_visible = \
            browser.find_element(By.CSS_SELECTOR, '.center .ng-binding:nth-child(2)')
        assert balance_visible.text == str(balance), 'неверный баланс'

    def transactions(self, browser, browser_name):
        select_transactions = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[ng-class="btnClass1"]')))
        select_transactions.click()

        headings = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'table a')))

        values_table = \
            WebDriverWait(browser, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tbody td')))
        values_tab = [i.text for i in values_table]

        data = [[i.text for i in headings]] + [values_tab[i:i + 3] for i in range(0, len(values_tab), 3)]
        new_data = self.data_format(data)

        self.generate_and_attach_transaction_report(new_data, browser_name)

    def data_format(self, data):
        for i in data[1:]:
            d_spl = re.split(' |, |:', i[0])
            d_join = f'{d_spl[1]} {d_spl[0]} {d_spl[2]} {d_spl[3] if d_spl[-1] == "AM" else int(d_spl[3]) + 12}:{d_spl[4]}:{d_spl[5]}'
            i[0] = d_join
        return data

    def generate_and_attach_transaction_report(self, transactions, browser_name):
        file = f'allure-results/Transaction_table_{browser_name}.csv'

        self.write_transactions_to_csv(transactions, file)

        self.attach_csv_report(file)

    def write_transactions_to_csv(self, transactions, file):
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for transaction in transactions:
                writer.writerow(transaction)

    def attach_csv_report(self, file):
        with open(file, 'rb') as csvfile:
            allure.attach(csvfile.read(), name='Transaction Report', attachment_type=allure.attachment_type.CSV)
