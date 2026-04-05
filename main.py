from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

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

# RESET FOR NEXT TEST
driver.get("https://www.saucedemo.com/")

# RELOGGING IN
login(driver, "standard_user")
wait_for_login_result(driver)

# SORTING
dropdown_locator = (By.CLASS_NAME, "product_sort_container")

options = [
    "Name (A to Z)",
    "Name (Z to A)",
    "Price (low to high)",
    "Price (high to low)"
]
for option in options:
    dropdown = driver.find_element(*dropdown_locator)
    Select(dropdown).select_by_visible_text(option)

    # Get names
    items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names = [item.text for item in items]

    # Get prices
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(p.text.replace("$", "")) for p in prices]

    result = False

    # Check sorting
    if option == "Name (A to Z)":
        result = names == sorted(names)

    elif option == "Name (Z to A)":
        result = names == sorted(names, reverse=True)

    elif option == "Price (low to high)":
        result = prices == sorted(prices)

    elif option == "Price (high to low)":
        result = prices == sorted(prices, reverse=True)

    # Print result
    print(f"{option} → {'PASS' if result else 'FAIL'}")

# ADDING ITEMS
driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-bike-light").click()
driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-bolt-t-shirt").click()
driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-fleece-jacket").click()
driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-onesie").click()
driver.find_element(By.CSS_SELECTOR,r"#add-to-cart-test\.allthethings\(\)-t-shirt-\(red\)").click()


# VERIFY IF ITEMS ARE IN THE CART
cart = int(driver.find_element(By.CLASS_NAME, "shopping_cart_link").text)
if cart == 6:
    print("Passed! All items was successfully added to the cart")
else:
    print("Failed! Items are not in the cart")


# CLOSE BROWSER
driver.quit()