# from selenium import webdriver 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

meet_sign_in_link = "https://accounts.google.com/v3/signin/identifier?dsh=S722429235%3A1677302391875669&continue=https%3A%2F%2Fmeet.google.com&ltmpl=meet&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AWnogHeN5XwzJ28EaHAhQnC4iq8zB8Mh1zQdEJU424Ugw2SSw5FF3WrHgVB-u6xnXICyzb93xPn46w"
email_box_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
email_next_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button"
password_box_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
dismiss_btn_path = "/html/body/div/div[3]/div[2]/div/div[2]/button"
join_btn_path = "/html/body/div[1]/c-wiz/div/div/div[13]/div[3]/div/div[1]/div[4]/div/div/div[2]/div/div[2]/div[1]/div[1]/button"
password_next_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button"

URL = "https://meet.google.com/xed-kqob-zcf"


def load_credentials():
    f = open('credentials.json')
    data = json.load(f)
    return data.get("email"), data.get("password")


def setup_selenium_driver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
    })
    service = Service("chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)


class Attend:
    def __init__(self, **kwargs):
        self.url = kwargs.get("google_meet_url", None)
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.browser = setup_selenium_driver()

    def authenticate(self):
        browser = self.browser
        browser.get(meet_sign_in_link)
        time.sleep(2)
        email_box = browser.find_element("xpath", email_box_path)
        email_next_btn = browser.find_element("xpath", email_next_path)
        email_box.send_keys(self.email)
        email_next_btn.click()
        time.sleep(2)
        pass_box = browser.find_element("xpath", password_box_path)
        pass_next_btn = browser.find_element("xpath", password_next_path)
        pass_box.send_keys(self.password)
        pass_next_btn.click()

    def join_meeting(self):
        self.authenticate()
        time.sleep(2)
        browser = self.browser
        browser.get(self.url)
        time.sleep(2)
        dismiss_button = browser.find_elements("xpath", dismiss_btn_path)
        if len(dismiss_button):
            dismiss_button[0].click()
        else:
            print("No element does not exist yet")
        time.sleep(2)
        join_button = browser.find_elements("xpath", join_btn_path)
        if len(join_button):
            join_button[0].click()
        else:
            print("No JOIN ELEMENT does not exist yet")


email, password = load_credentials()
bot = Attend(google_meet_url=URL, email=email, password=password)
bot.join_meeting()
