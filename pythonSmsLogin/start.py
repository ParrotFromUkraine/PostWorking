import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Конфигурация
API_KEY = "c39A3809b434A4AA512361d8bcbbAe66"
SMS_ACTIVATE_URL = "https://sms-activate.org/stubs/handler_api.php"
PASSWORD = "your_new_password_here"  # Замените на ваш пароль
TIKTOK_URL = "https://www.tiktok.com/login/phone/forget-password"

def get_phone_number():
    params = {
        "api_key": API_KEY,
        "action": "getNumber",
        "service": "tk",  # TikTok
        "country": "0"  # 0 - автоматический выбор страны
    }
    
    response = requests.get(SMS_ACTIVATE_URL, params=params)
    if response.text.startswith("ACCESS_NUMBER"):
        data = response.text.split(":")
        activation_id = data[1]
        phone_number = data[2]
        return activation_id, phone_number
    else:
        raise Exception(f"Не удалось получить номер: {response.text}")

def get_sms_code(activation_id):
    params = {
        "api_key": API_KEY,
        "action": "getStatus",
        "id": activation_id
    }
    
    for _ in range(20):  # Проверяем 20 раз с интервалом в 5 секунд
        time.sleep(5)
        response = requests.get(SMS_ACTIVATE_URL, params=params)
        if response.text.startswith("STATUS_OK"):
            return response.text.split(":")[1]
    
    raise Exception("Не удалось получить SMS код")

def save_to_file(phone_number, password):
    with open("numbers.txt", "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | {phone_number} | {password}\n")

def main():
    # Инициализация Chrome
    driver = webdriver.Chrome()
    driver.get(TIKTOK_URL)
    
    try:
        # Получаем номер телефона
        activation_id, phone_number = get_phone_number()
        print(f"Получен номер: {phone_number}, ID активации: {activation_id}")
        
        # Вводим номер телефона
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Номер телефона']"))
        )
        phone_input.send_keys(phone_number)
        
        # Нажимаем кнопку отправки кода
        send_code_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        send_code_btn.click()
        
        # Проверяем наличие ошибок
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".error-message")
            raise Exception(f"Ошибка на странице: {error_element.text}")
        except:
            pass  # Ошибок нет, продолжаем
        
        # Получаем SMS код
        sms_code = get_sms_code(activation_id)
        print(f"Получен SMS код: {sms_code}")
        
        # Вводим SMS код
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Код подтверждения']"))
        )
        code_input.send_keys(sms_code)
        
        # Вводим новый пароль
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Новый пароль']"))
        )
        password_input.send_keys(PASSWORD)
        
        # Нажимаем кнопку подтверждения
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        confirm_btn.click()
        
        # Сохраняем данные
        save_to_file(phone_number, PASSWORD)
        print("Успешно! Данные сохранены в numbers.txt")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
