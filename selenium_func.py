import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from chrome import open_chrome_debug
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import random

class SeleniumDebugger:
    def __init__(self):
        self.driver = None
        self.stop_flag = False

    # ---------- CONNECT ----------
    def connect_selenium_debug(self, url=None, port=9222):
        if self.driver:
            print("[DEBUG] Chrome already connected")
            return self.driver

        print("[DEBUG] Opening Chrome debug:", url)
        open_chrome_debug(url, port)
        time.sleep(2)

        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{port}"
        )

        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        print("[DEBUG] Selenium connected")
        return self.driver

    # ---------- URL CHECK ----------
    def is_on_zone_page(self):
        try:
            url = self.driver.current_url
            print("[DEBUG] Current URL:", url)
            return "zones.php" in url
        except Exception as e:
            print("[DEBUG] URL check error:", e)
            return False

    # ---------- FAST CLICK ----------
    def fast_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    # ---------- BOOKING FLOW ----------
    def select_zone(self, zone):
        while True:
            try:
                area = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'area[href*="{zone}"]'))
                )
                self.driver.execute_script("""
                    let event = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    arguments[0].dispatchEvent(event);
                """, area)
                break
            except Exception as e:
                print(f"ERROR เข้าเว็บหรือคลิกไม่ได้:, ลองใหม่อีกครั้ง")
                time.sleep(1)


        seat_count = 1
        selected_count = 0
        while True:
            try:
                table = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "tableseats"))
                )
                seats = table.find_elements(By.CSS_SELECTOR, "div.seatuncheck")
                random.shuffle(seats)

                for seat_div in seats:
                    seat_id = seat_div.get_attribute("id")
                    try:
                        self.fast_click(seat_div)
                        print(f"เลือกที่นั่ง: {seat_id}")
                        selected_count += 1
                        if selected_count >= seat_count:
                            break
                    except Exception as e:
                        print(f"คลิกที่นั่ง {seat_id} ไม่ได้: {e}")
                        continue

                if selected_count == 0:
                    print("ไม่มีที่นั่งว่างเลย -> refresh 10s")
                    time.sleep(3)
                    self.driver.refresh()
                    continue

            except Exception as e:
                print(f"เกิดข้อผิดพลาดตอนเลือกที่นั่ง")
                time.sleep(3)
                self.driver.refresh()
                continue

            
            try:
                seat_selected = self.driver.find_element(By.ID, "seat_selected").text.strip()
                seat_m_selected = self.driver.find_element(By.ID, "seat_m_selected").text.strip()

                if seat_selected or seat_m_selected:
                    print(f"ที่นั่งถูกเลือก: {seat_m_selected} or {seat_selected} -> กด Submit")

                    try:
                        button_submit = self.driver.find_element(By.CSS_SELECTOR, ".btn-red.btn-main-action.w-auto.right")
                        self.fast_click(button_submit)
                    except:
                        try:
                            button_submit_inline = self.driver.find_element(By.CSS_SELECTOR, ".btn-red.btn-main-action.w-auto.d-inline-block.d-lg-block")
                            self.fast_click(button_submit_inline)
                        except:
                            print("ไม่พบปุ่ม Submit")



                    try:
                        WebDriverWait(self.driver, 3).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".popup.popup-content.popup-l"))
                        )
                    except TimeoutException:
                        print("⚠️ เจอ popup หลัง Submit -> refresh")
                        self.driver.refresh()
                        # button_close = driver.find_element(By.CSS_SELECTOR, ".btn-red w-auto")
                        # button_close.click()
                        # selected_count = 0
                        continue

                    print("🎉 กด Submit สำเร็จ!")
                    break
                else:
                    print("ยังไม่มีที่นั่งถูกเลือก -> refresh")
                    

                    self.driver.refresh()
                    time.sleep(1)
                    selected_count = 0

            except Exception as e:
                print(f"ไม่พบปุ่ม Submit หรือที่นั่ง")
                self.driver.refresh()
                selected_count = 0