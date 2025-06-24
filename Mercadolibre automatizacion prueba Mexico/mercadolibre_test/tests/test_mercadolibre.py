import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def take_screenshot(driver, step):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/{step}.png")

def test_mercadolibre_search(driver):
    # Paso 1: Entrar al sitio
    driver.get("https://www.mercadolibre.com")
    take_screenshot(driver, "1_home")

    # Paso 2: Seleccionar México
    driver.find_element(By.XPATH, "//a[contains(@href, '/mexico')]").click()
    time.sleep(2)
    take_screenshot(driver, "2_mexico")

    # Paso 3: Buscar "playstation 5"
    search_input = driver.find_element(By.NAME, "as_word")
    search_input.send_keys("playstation 5")
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)
    take_screenshot(driver, "3_busqueda")

    # Paso 4: Filtrar por "Nuevos"
    driver.find_element(By.XPATH, "//span[text()='Nuevo']").click()
    time.sleep(2)
    take_screenshot(driver, "4_nuevos")

    # Paso 5: Filtrar por "CDMX"
    driver.find_element(By.XPATH, "//span[contains(text(), 'Distrito Federal')]").click()
    time.sleep(2)
    take_screenshot(driver, "5_cdmx")

    # Paso 6: Ordenar por "Mayor precio"
    order_button = driver.find_element(By.CLASS_NAME, "andes-dropdown__trigger")
    order_button.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Mayor precio')]").click()
    time.sleep(3)
    take_screenshot(driver, "6_ordenado")

    # Paso 7: Obtener nombre y precio de los 5 primeros
    items = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__content-wrapper")[:5]
    print("\nPrimeros 5 productos:")
    for i, item in enumerate(items, 1):
        title = item.find_element(By.CSS_SELECTOR, "h2").text
        price = item.find_element(By.CSS_SELECTOR, ".price-tag-fraction").text
        print(f"{i}. {title} - ${price}")
    take_screenshot(driver, "7_resultados")
