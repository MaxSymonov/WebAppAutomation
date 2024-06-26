from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
import time

class MediaPage:
    def __init__(self, driver):
        self.driver = driver
        self.media_tab = (By.LINK_TEXT, "Media")
        self.incidents_tab = (By.LINK_TEXT, "Videos")
        self.delete_footage_button = (By.XPATH, "(//button[contains(@class,'btn btn-default')])[2]")
        self.delete_incident_button = (By.XPATH, "//button[@data-original-title='Delete video']")
        self.confirm_delete_incident_button = (By.XPATH, "//button[text()='Button']")
        self.last_video_duration = (By.XPATH, "//td[@class='col-sm-8']")
        # Video options
        self.create_new_incident = (By.XPATH, "//a[@class='btn video-new-incident']")
        self.add_media_to_existing_incident = (By.XPATH, "//a[@class='btn video-add-to-incident']")
        self.delete_media = (By.XPATH, "//button[@class='btn somebutton']")
        self.confirm_delete = (By.XPATH, "//button[text()='yes']")
        self.dropdown_menu = (By.XPATH, "//button[@class='btn dropdown-toggle']")
        # New incident fields
        self.incident_title = (By.ID, "inputCustom55")
        self.reference_code = (By.ID, "inputCustom59")
        self.notes = (By.ID, "inputCustom60")
        self.create_incident_button = (By.XPATH, "//button[text()='Create stuff']")

    def open_media_tab(self):
        self.driver.find_element(*self.media_tab).click()

    def verify_last_video_duration(self, expected_duration):
        actual_duration = self.driver.find_element(*self.last_video_duration).text
        assert actual_duration == expected_duration, f"Expected '{expected_duration}', but got '{actual_duration}'"

    def verify_video_options(self):
        assert self.driver.find_element(*self.create_new_incident).is_displayed(), "Create new incident option is not displayed"
        assert self.driver.find_element(*self.add_media_to_existing_incident).is_displayed(), "Add media to existing incident option is not displayed"
        assert self.driver.find_element(*self.delete_media).is_displayed(), "Delete media option is not displayed"
        assert self.driver.find_element(*self.dropdown_menu).is_displayed(), "Dropdown toggle option is not displayed"

    def create_new_incident_add(self, title, reference_code, notes):
        self.driver.find_element(*self.create_new_incident).click()
        time.sleep(2)
        self.driver.find_element(*self.incident_title).send_keys(title)
        time.sleep(1)
        self.driver.find_element(*self.reference_code).send_keys(reference_code)
        time.sleep(1)
        self.driver.find_element(*self.notes).send_keys(notes)
        time.sleep(1)

        self.driver.find_element(*self.create_incident_button).click()
        time.sleep(2)

        self.driver.find_element(*self.delete_incident_button).click()
        time.sleep(2)

        self.driver.switch_to.active_element

        self.driver.find_element(*self.confirm_delete_incident_button).click()

        time.sleep(2)

        self.driver.switch_to.active_element

    def delete_recorded_footage(self):
        self.driver.refresh()
        # alert = Alert(self.driver)
        # alert.accept()

        time.sleep(2)

        self.driver.find_element(*self.media_tab).click()
        time.sleep(2)
        delete_buttons = self.driver.find_elements(*self.delete_media)
        for _ in range(len(delete_buttons)):
            try:
                self.driver.find_element(*self.delete_media).click()
                time.sleep(1)
                self.driver.find_element(*self.confirm_delete).click()
                time.sleep(1)
            except NoSuchElementException:
                print("Finished removing recorded footage after test")
                break

