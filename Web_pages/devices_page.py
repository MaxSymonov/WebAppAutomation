from selenium.webdriver.common.by import By
import yaml
import time

class DevicesPage:
    def __init__(self, driver, test_data_file):
        self.driver = driver        
        self.devices_tab = (By.LINK_TEXT, "Devices")
        with open(test_data_file, 'r') as file:
            self.test_data = yaml.safe_load(file)

        self.find_devices = (By.XPATH, "//button[text()='Find devices']")
        self.return_device = (By.XPATH, "//button[@data-original-title='Return Device']")
        self.assign_device = (By.XPATH, "//button[@data-original-title='Assign Device']")
        self.operator_name = (By.XPATH, "//input[@class='form-control tt-input']")
        self.assign_device_confirm = (By.XPATH, "//button[text()='Assign Device']")
        self.status = (By.XPATH, "//span[@class='js-status-text status-text']")

    def assign_device_to_user(self):
        self.driver.find_element(*self.devices_tab).click()
        time.sleep(2)
        username = self.test_data['username']
        self.driver.find_element(*self.find_devices).click()
        time.sleep(2)

        return_device_elements = self.driver.find_elements(*self.return_device)
        assign_device_elements = self.driver.find_elements(*self.assign_device)

        if return_device_elements:
            return_device_elements[0].click()
            time.sleep(2)
            assign_device_elements = self.driver.find_elements(*self.assign_device)
            if assign_device_elements:
                assign_device_elements[0].click()
        elif assign_device_elements:
            assign_device_elements[0].click()

        time.sleep(2)

        self.driver.switch_to.active_element

        self.driver.find_element(*self.operator_name).send_keys(username)
        time.sleep(2)
        self.driver.find_element(*self.assign_device_confirm).click()
        time.sleep(2)

        status_text = self.driver.find_element(*self.status).text

        assert status_text == 'Ready', f"Expected status to be 'Ready', but got '{status_text}'"

        


