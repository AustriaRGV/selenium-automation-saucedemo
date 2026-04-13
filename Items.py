from popup_handler import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

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

driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

#Return shopping button in cart
driver.find_element(By.CSS_SELECTOR, "#continue-shopping").click()
WebDriverWait(driver, 10).until(
    ec.url_contains("inventory")
)
assert "inventory" in driver.current_url, "Failed!"
print("Passed! Continue Shopping button working properly")

#Remove items
driver.find_element(By.CSS_SELECTOR, r"#remove-test\.allthethings\(\)-t-shirt-\(red\)").click()

WebDriverWait(driver, 10).until(
    ec.invisibility_of_element_located((By.CSS_SELECTOR, r"#remove-test\.allthethings\(\)-t-shirt-\(red\)")
    )
)
items = driver.find_elements(By.CSS_SELECTOR, r"#remove-test\.allthethings\(\)-t-shirt-\(red\)")
assert len(items) == 0, "Failed! The item was not removed"
print("Passed! The item was successfully removed")
# CLOSE BROWSER
driver.quit()