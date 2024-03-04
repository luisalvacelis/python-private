import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def start_driver():
    driver = webdriver.Chrome()
    return driver

def login(driver):
    driver.get("https://web.whatsapp.com/")
    input("Presiona Enter después de escanear el código QR...")
    print("Iniciando sesión...")

def validar_numeros(driver, numeros):
    for numero in numeros:
        try:
            # Buscar el chat del número
            search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="selectable-text copyable-text iq0m558w g0rxnol2"]')))
            search_box.clear()
            search_box.send_keys(numero)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)

            # Validar si el chat se ha abierto
            if EC.presence_of_element_located((By.XPATH, '//div[@class="_2Ts6i _2xAQV"]')):
                print(f"El chat con {numero} se ha abierto. Activo.")
            else:
                print(f"No se pudo abrir el chat con {numero}. Inactivo o inexistente.")
        except Exception as e:
            print(f"Error al procesar el número {numero}: {e}")

if __name__ == "__main__":
    numeros = ["+51940377852", "+51993465801", "+51926981818"]
    driver = start_driver()
    login(driver)
    validar_numeros(driver, numeros)
    driver.quit()
