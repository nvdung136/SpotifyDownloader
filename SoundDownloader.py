from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os 
import time


def main():
    (wait, BRWSdriver) = initiation()
    print("Giving the song URL: ... ")
    songURL = input()
    SearchnDownload(wait,BRWSdriver,songURL,1)

#Initiate a browser instant and setup basic wait instant
def initiation():
    load_dotenv()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    spath = Service(os.getenv("BROWSER_DRIVER"))
    BRWSinst = webdriver.Chrome(service=spath,options=chrome_options)
    BRWSinst.get("https://spotifydown.com/")
    wait = WebDriverWait(BRWSinst,30)
    return (wait, BRWSinst)

#Execute download procedure then open and shift focuse to a new tab
def SearchnDownload(wait: WebDriverWait,DRV: webdriver.Chrome,SongURL: str,tabNo: int):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"searchInput")))
    FillBox = DRV.find_element(By.CLASS_NAME,"searchInput")
    FillBox.send_keys(SongURL)
    time.sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text() = 'Download']")))
    print('Found button')
    time.sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text() = 'Download']"))).click()
    print('Button clicked')
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"w-24"))).click()
    time.sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@href, 'blob:https://spotifydown.com/')]")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@href, 'blob:https://spotifydown.com/')]"))).click()
    DRV.execute_script("window.open('{0}', '_blank');".format("https://spotifydown.com/"))
    DRV.switch_to.window(DRV.window_handles[tabNo])
    

if __name__ == "__main__":
    main()
