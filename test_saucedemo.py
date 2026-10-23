import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
TIMEOUT = 20


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    drv.set_window_size(1920, 1080)
    yield drv
    drv.quit()


def wait(driver):
    return WebDriverWait(driver, TIMEOUT)


def js_click(driver, by, value):
    """Chờ phần tử có mặt trong DOM rồi click bằng JavaScript."""
    el = wait(driver).until(EC.presence_of_element_located((by, value)))
    driver.execute_script("arguments[0].click();", el)


def login(driver, username, password):
    driver.get(BASE_URL)
    wait(driver).until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def wait_for_inventory(driver):
    wait(driver).until(EC.url_contains("inventory.html"))
    # Chờ danh sách sản phẩm render xong
    wait(driver).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))


def wait_for_error(driver):
    return wait(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )


def test_tc01_login_success(driver):
    login(driver, "standard_user", "secret_sauce")
    wait_for_inventory(driver)
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"


def test_tc02_login_wrong_password(driver):
    login(driver, "standard_user", "wrong_password")
    error = wait_for_error(driver)
    assert "Username and password do not match" in error.text


def test_tc03_login_locked_out_user(driver):
    login(driver, "locked_out_user", "secret_sauce")
    error = wait_for_error(driver)
    assert "locked out" in error.text.lower()


def test_tc04_login_empty_username(driver):
    login(driver, "", "secret_sauce")
    error = wait_for_error(driver)
    assert "Username is required" in error.text


def test_tc05_add_product_to_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    wait_for_inventory(driver)

    js_click(driver, By.ID, "add-to-cart-sauce-labs-backpack")

    # Nút đổi thành "Remove" nghĩa là sản phẩm đã vào giỏ
    wait(driver).until(EC.presence_of_element_located((By.ID, "remove-sauce-labs-backpack")))
    # Chờ badge hiện đúng số "1"
    wait(driver).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))

    assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "1"


def test_tc06_logout(driver):
    login(driver, "standard_user", "secret_sauce")
    wait_for_inventory(driver)

    js_click(driver, By.ID, "react-burger-menu-btn")
    wait(driver).until(EC.presence_of_element_located((By.ID, "logout_sidebar_link")))
    js_click(driver, By.ID, "logout_sidebar_link")

    login_btn = wait(driver).until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert login_btn.is_displayed()
