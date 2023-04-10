import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException


class CathayBank:
    def __init__(self):
        mobile_emulation = {"deviceName": "iPhone X"}
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_website(self, url):
        try:
            self.driver.get(url)
            time.sleep(5)
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

    def screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)
            logging.info(f'Screenshot saved as {filename}')
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

    def credit_card_menu(self):
        # 左上選單 > 個人金融 > 產品介紹 > 信用卡列表
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div[1]'))).click()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div'))).click()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/div'))).click()
            time.sleep(5)
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

        # Count the num of submenu under credit card
        try:
            card_parentmenu = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[2]')))
            card_submenu = card_parentmenu.find_elements(By.CLASS_NAME, 'cubre-a-menuLink')
            num_card_submenu = len(card_submenu)
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

        return num_card_submenu

    def credit_card_details(self):
        # 個人金融 > 產品介紹 > 信用卡列表 > 卡片介紹
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lnk_Link"]'))).click()
            target_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div/div/div[1]/div/div/a[6]')
            actions = ActionChains(self.driver)
            actions.move_to_element(target_element).click_and_hold().perform()
            inactive_card_tab = target_element.click()
            time.sleep(5)
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

        # Count the num of inactive credit card
        try:
            inactive_card_sec = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/article/section[6]/div/div[2]/div/div[1]')
            inactive_card_item = inactive_card_sec.find_elements(By.CLASS_NAME, 'cubre-m-compareCard__title')
            num_inactive_card = len(inactive_card_item)
            tab_sec = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/article/section[6]/div/div[2]/div/div[2]')
            for i in range(0, num_inactive_card):
                tab = tab_sec.find_elements(By.CLASS_NAME, 'swiper-pagination-bullet')[i].click()
                self.driver.save_screenshot(f'cathaybk_inactive_card-{i:03d}.png')
                logging.info(f'Screenshot saved as cathaybk_inactive_card-{i:03d}.png')
                time.sleep(1)
        except WebDriverException as e:
            logging.error(f"An exception occurred: {e}")
            raise

        return num_inactive_card

    def close_browser(self):
        self.driver.quit()


# logging
FORMAT = '%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(
    level=logging.INFO,
    format = FORMAT,
    datefmt=DATE_FORMAT,
    filename='Logging.log'
)

# Start testing
# Step 1
cathay_bank = CathayBank()
cathay_bank.open_website("https://www.cathaybk.com.tw/cathaybk/")
cathay_bank.screenshot("cathaybk_homepage.png")

# Step 2
num_card_submenu = cathay_bank.credit_card_menu()
print('信用卡選單共有%d個項目' % num_card_submenu)
cathay_bank.screenshot("cathaybk_credit_card_submenu.png")

# Step 3
num_inactive_card = cathay_bank.credit_card_details()
print('已停發信用卡共有%d個' % num_inactive_card)

cathay_bank.close_browser()
