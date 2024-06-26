from selenium.webdriver.common.by import By
import yaml
import time

class LoginPage:
    def __init__(self, driver, test_data_file):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.sign_in_button_field = (By.ID, "sign-in")
        with open(test_data_file, 'r') as file:
            self.test_data = yaml.safe_load(file)

    def enter_credentials_and_login(self):
        username = self.test_data['username']        
        password = self.test_data['password']
        username_element = self.driver.find_element(*self.username_field)
        password_element = self.driver.find_element(*self.password_field)
        sign_in_button = self.driver.find_element(*self.sign_in_button_field)

        time.sleep(0.5)
        
        username_element.send_keys(username)    

        time.sleep(0.5)

        password_element.send_keys(password)
        
        time.sleep(1)

        sign_in_button.click()