import time
import pandas as pd
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def start_driver(path): 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--safebrowsing.enabled=true")
    prefs = {
        "download.default_directory": path,
        "download.directory_upgrade": True,
        "extensions_to_open": ""
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def delete_cache(driver):
    driver.delete_all_cookies()

def open_page(driver,username,password,date_from,date_to,path):
    try:
        driver.get("https://solucionesreclamos.com/siac_desborde/app/vista/login_lh/index_sc.php")
        time.sleep(2)
        input_username=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"txtusuario")))
        input_password=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"txtpassword")))
        button_join=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"btnacceder")))

        input_username.click()
        input_username.send_keys(username)
        
        input_password.click()
        numpad=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"numpad")))
        buttons=numpad=numpad.find_elements(By.CSS_SELECTOR,"button")
        
        for value in password:
            for button in buttons:
                if button.text==value:
                    button.click()
                    time.sleep(0.5)
                    break
        time.sleep(2)
        button_join.click()
        time.sleep(10)
        export(driver,date_from,date_to,path)
    except Exception as e:
        print('Error:',e)
    finally:
        driver.quit()

def export(driver,date_from,date_to,path):
    try:
        a_gestion=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"gestion")))
        a_gestion.click()

        item_casos_reclamos=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".show > .dropdown-item:nth-child(1)")))
        item_casos_reclamos.click()
        time.sleep(2)

        script = """
        var datepickerElement = document.querySelector('.datepicker');
        if (datepickerElement) {
            datepickerElement.parentNode.removeChild(datepickerElement);
        }
        """

        input_date_from=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"desde")))
        input_date_from.clear()
        driver.execute_script(f"arguments[0].value = '{date_from}';", input_date_from)
        driver.execute_script(script)

        input_date_to=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"hasta")))
        input_date_to.clear()
        driver.execute_script(f"arguments[0].value = '{date_to}';", input_date_to)
        driver.execute_script(script)

        primer_radio_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="buscbase"]:first-of-type')))
        primer_radio_button.click()
        
        time.sleep(2)

        button_search=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"buscar")))
        button_search.click()
        time.sleep(2)
        button_export=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"exportar")))
        button_export.click()
        time.sleep(20)
        order_columns(path)
    except Exception as e:
        print('Error:',e)
    finally:
        driver.quit()

def order_columns(path):
    file_paths=glob.glob(path+"\*.csv")
    list_columns = ["CALC_SISTEMA", "FLAG_RECLAMO_PRINCIPAL", "NUMERO_RECLAMO", "CASO_NUMERO",
                      "CALC_FECHA_RECLAMO", "CALC_FECHA_HORA_RECLAMO", "MONTO_RECLAMADO_CARGO",
                      "MONTO_RECLAMADO", "MOTIVO1", "MOTIVO3", "MEDIO_UTILIZADO_INFO",
                      "TELEFONO", "CLIENTE_KEY", "TIPO_DOCUMENTO_RECLAMANTE",
                      "NUMERO_DOCUMENTO_RECLAMANTE", "APELLIDOS_RECLAMANTE",
                      "NOMBRES_RECLAMANTE", "DIRECCION_PREFERIDA", "CALC_DEPARTAMENTO_INEI",
                      "CALC_PROVINCIA_INEI", "CALC_DISTRITO_INEI", "ID", "FECHA_CREACION_CASO",
                      "FECHA_ULTIMA_MODIFICACION", "MODIFICADO_POR", "MOTIVO_REAL",
                      "SUBTIPIFICACION", "ESTADO_RECLAMO", "RESULTADO_DEL_RECLAMO", "PAUTA1",
                      "PAUTA2", "ORDER_ID_1", "MONTO_TOTAL", "ESTADO_ACTUAL", "FLAG_APAGADO_URA",
                      "FLAG_ROBOT_LIQUIDACION", "FECHA_FIN_ROBOT", "RESOLUCION",
                      "FECHA_SOLICITUD_BAJA", "TIPO_RECLAMANTE", "FECHA_ORDEN", "TRANSACCION",
                      "ESTADO_TICKETDOIT", "ESTADO_ORDER_ID", "FECHA_DESCUENTO", "TIPO_DESCUENTO"]
    dfs=[]
    for file in file_paths:
        df=pd.read_csv(file)
        df=df[list_columns]
        dfs.append(df)
    merged_df = pd.concat(dfs)
    merged_df.to_csv(path+"\datos_ordenados.csv", index=False)

def execute_script(path,username,password,date_from,date_to):
    driver=start_driver(path)
    if driver:
        delete_cache(driver)
        open_page(driver,username,password,date_from,date_to,path)

if __name__ == '__main__':
    path_to_download_reports = r"C:\Users\Luis Alva\Desktop\reportes"
    username="46171647"
    password=['4','6','1','7','1','6','4','6']
    date_from="25-02-2024"
    date_to="27-02-2024"
    execute_script(path_to_download_reports,username,password,date_from,date_to)