from popup_handler import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


# SETUP DRIVER
driver = create_driver()
driver.get("https://www.saucedemo.com/")
wait = WebDriverWait(driver, 5)

#LOGGING IN
username = "standard_user"
password = "secret_sauce"
username_field = driver.find_element(By.CSS_SELECTOR, "#user-name").send_keys(username)
password_field = driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "#login-button").click()

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

driver.quit()

