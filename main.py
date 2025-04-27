import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Функция создания драйвера
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')

    # Включение headless режима
    chrome_options.add_argument('--headless')  # Это делает браузер невидимым

    return webdriver.Chrome(options=chrome_options)


# Парсинг события
def parse_event():
    driver = create_driver()
    try:
        driver.get("https://www.etihadarena.ae/en/event-booking/2025-turkish-airlines-euroleague-f4")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Даем время для загрузки

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-cta-golden'))
        )

        button_block = driver.find_element(By.CLASS_NAME, 'btn-cta-golden')
        button_text = button_block.find_element(By.TAG_NAME, 'a').text.strip()

        status = "BUY TICKETS" if button_text == "BUY TICKETS" else "SOLD OUT"

        # Записываем статус в базу данных
        conn = sqlite3.connect('event_status.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS status (status TEXT)")
        c.execute("DELETE FROM status")  # Очищаем таблицу перед добавлением нового
        c.execute("INSERT INTO status (status) VALUES (?)", (status,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Ошибка при парсинге события: {e}")
    finally:
        driver.quit()


# Основной цикл
def main():
    while True:
        parse_event()
        time.sleep(60)  # Проверка каждую минуту


if __name__ == '__main__':
    main()

