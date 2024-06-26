import time
import unittest
import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import ChromeOptions, EdgeOptions, FirefoxOptions
import yaml
import os
import subprocess
from selenium.webdriver.common.alert import Alert

import Web_pages.login_page as login
import Web_pages.media_page as media
import Web_pages.devices_page as devices

"""
Install dependencies:
pip install selenium
pip install webdriver-manager
pip install pyyaml
"""


start_recording = '/mnt/pss/rootfs/usr/bin/busctl call com.edesix.Recorder /com/edesix/Recorder/Ui com.edesix.Recorder.Ui StartRecording ss Manual INTERNAL_BUTTONS'
stop_recording = '/mnt/pss/rootfs/usr/bin/busctl call com.edesix.Recorder /com/edesix/Recorder/Ui com.edesix.Recorder.Ui StopRecording ss StopButtonPressed INTERNAL_BUTTONS'

def get_driver():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    test_data_file_path = os.path.join(script_dir, 'web_testdata.yaml')
    with open(test_data_file_path, 'r') as file:
        test_data = yaml.safe_load(file)

    browser_name = test_data['browser_name']

    if browser_name == 'Chrome':
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        ChromeDriverManager().install()
        driver = webdriver.Chrome(options=options)
        return driver
    elif browser_name == 'Edge':
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        EdgeChromiumDriverManager().install()
        driver = webdriver.Edge(options=options)
        return driver
    elif browser_name == 'Firefox':
        options = FirefoxOptions()
        GeckoDriverManager().install()
        driver = webdriver.Firefox(options=options)
        return driver
    else:
        raise ValueError(f"Unsupported browser: {browser_name}. Supported browsers are: Chrome, Edge, Firefox")

class Tests(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        global driver
        warnings.filterwarnings("ignore")

    def setUp(self) -> None:
        self.driver = get_driver()
        self.driver.maximize_window()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        test_data_file_path = os.path.join(script_dir, 'web_testdata.yaml')
        self.login_page = login.LoginPage(self.driver, test_data_file_path)
        self.devices_page = devices.DevicesPage(self.driver, test_data_file_path)
        self.driver.get('http://localhost:9080/')

    def tearDown(self) -> None:    
        Logger.logger_underline('Deleting recorded footage after test')
        media.MediaPage(self.driver).delete_recorded_footage()



    @classmethod
    def tearDownClass(cls) -> None:
        if cls.driver is not None:
            try:
                cls.driver.quit()
            except Exception as e:
                Logger.logger_warn(f"An error occurred while stopping session: {str(e)}")

    '''
    Add new tests here. Any method that starts with 'test_' prefix will be treated as a new test. 
    '''

    def test_1_assign_device_to_user(self):
       Logger.logger_step(1, 'Log in into the app')
       Functions.verify_title_contains(self.driver, 'Login')
       self.login_page.enter_credentials_and_login()
       time.sleep(2)

       Functions.send_adb_command('root')

       Logger.logger_step(2, 'Assign or re-assign device to the configured user')

       self.devices_page.assign_device_to_user()

       pass

    def test_2_record_video_verify_stuff(self):
       Logger.logger_step(1, 'Log in into the app')
       Functions.verify_title_contains(self.driver, 'Login')
       self.login_page.enter_credentials_and_login()
       time.sleep(2)

       Functions.send_adb_command('root')

       Logger.logger_step(2, 'Record a 10 - seconds long video')

       Functions.send_adb_shell_command(start_recording)

       time.sleep(10.5)

       Functions.send_adb_shell_command(stop_recording)

       time.sleep(2)

       Logger.logger_step(3, 'Open Media tab')
       
       media.MediaPage(self.driver).open_media_tab()

       time.sleep(5)

       Logger.logger_step(4, 'Verify added video duration')

       media.MediaPage(self.driver).verify_last_video_duration('10s')

       
       Logger.logger_step(5, 'Verify video options')

       media.MediaPage(self.driver).verify_video_options()       
       
       pass

    def test_3_record_video_add_incident(self):
       Logger.logger_step(1, 'Log in into the app')
       Functions.verify_title_contains(self.driver, 'Login')
       self.login_page.enter_credentials_and_login()
       time.sleep(2)

       Functions.send_adb_command('root')

       time.sleep(2)

       Logger.logger_step(2, 'Record a 5 - seconds long video')

       Functions.send_adb_shell_command(start_recording)

       time.sleep(6)

       Functions.send_adb_shell_command(stop_recording)

       time.sleep(2)

       Logger.logger_step(3, 'Open Media tab')
       
       media.MediaPage(self.driver).open_media_tab()

       time.sleep(2)

       Logger.logger_step(4, 'Crete new incident with recorded video')

       media.MediaPage(self.driver).create_new_incident_add('Test incident', '12345', 'The framework actually works - WOW!')

       pass

    

class Functions:    

    @staticmethod
    def refresh_page(self):
        self.driver.refresh()
        alert = Alert(self.driver)
        alert.accept()

    @staticmethod
    def send_adb_shell_command(command):
        full_command = f"adb shell {command}"
        subprocess.run(full_command, shell=True)

    @staticmethod
    def send_adb_command(command):
        os.system(f"adb {command}")

    @staticmethod
    def verify_page_title(driver, expected_title):
        actual_title = driver.title
        return actual_title == expected_title
    
    @staticmethod
    def verify_title_contains(driver, expected_substring):
        actual_title = driver.title
        return expected_substring in actual_title

class Logger:

    @staticmethod
    def logger_step(step_num, text):
        print(f"{PrintColors.PURPLE}{step_num}{' '}{text}{PrintColors.ENDCOLOR}")

    @staticmethod
    def logger_ok(text):
        print(f"{PrintColors.OKGREEN}{text}{PrintColors.ENDCOLOR}")

    @staticmethod
    def logger_warn(text):
        print(f"{PrintColors.WARNING}{text}{PrintColors.ENDCOLOR}")

    @staticmethod
    def logger_fail(text):
        print(f"{PrintColors.FAIL}{text}{PrintColors.ENDCOLOR}")

    @staticmethod
    def logger_bold(text):
        print(f"{PrintColors.BOLD}{text}{PrintColors.ENDCOLOR}")

    @staticmethod
    def logger_underline(text):
        print(f"{PrintColors.UNDERLINE}{text}{PrintColors.ENDCOLOR}")

class PrintColors:
    PURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    unittest.main()