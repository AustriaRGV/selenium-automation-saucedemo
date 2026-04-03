from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

# HANDLE CHROME POPUPS
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
})

# SETUP DRIVER
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.saucedemo.com/")
wait = WebDriverWait(driver, 5)
