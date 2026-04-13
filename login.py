from popup_handler import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# SETUP DRIVER
driver = create_driver()
driver.maximize_window()
driver.get("https://www.saucedemo.com/")
wait = WebDriverWait(driver, 5)

# LOGIN FUNCTION
def login(web_driver, user_name, password="secret_sauce"):
    local_wait = WebDriverWait(web_driver, 5)

    username_field = local_wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "#user-name"))
    )
    username_field.clear()
    username_field.send_keys(user_name)

    password_field = web_driver.find_element(By.CSS_SELECTOR, "#password")
    password_field.clear()
    password_field.send_keys(password)

    web_driver.find_element(By.CSS_SELECTOR, "#login-button").click()
    web_driver.find_element(By.TAG_NAME, "body").click()

# LOGOUT FUNCTION
def logout(web_driver, wait_obj):
    web_driver.find_element(By.CSS_SELECTOR, "#react-burger-menu-btn").click()
    logout_btn = wait_obj.until(
        ec.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_btn.click()

# TEST CASES
test_cases = [
    {"username": "", "expected": "fail"},
    {"username": "standard_user", "expected": "success"},
    {"username": "locked_out_user", "expected": "fail"},
    {"username": "problem_user", "expected": "success"},
    {"username": "performance_glitch_user", "expected": "success"},
    {"username": "error_user", "expected": "success"},
    {"username": "visual_user", "expected": "success"},
]

def wait_for_login_result(web_driver, timeout=3):
    local_wait = WebDriverWait(web_driver, timeout)
    return local_wait.until(
            lambda d: (
                    "inventory" in d.current_url or
                    d.find_elements(By.CSS_SELECTOR, "h3[data-test='error']")
            )
        )
# RUN TESTS
for case in test_cases:
    username = case["username"]
    expected = case["expected"]

    login(driver, username)
    wait_for_login_result(driver)
    if "inventory" in driver.current_url:
        print(f"{username or 'EMPTY'} → SUCCESS")
        logout(driver, wait)
    else:
        print(f"{username or 'EMPTY'} → FAILED")

driver.quit()