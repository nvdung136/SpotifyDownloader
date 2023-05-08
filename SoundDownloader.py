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
    BRWSinst.get("https://www.soundloaders.com/spotify-downloader/")
    wait = WebDriverWait(BRWSinst,10)
    return (wait, BRWSinst)

#Execute download procedure then open and shift focuse to a new tab
def SearchnDownload(wait: WebDriverWait,DRV: webdriver.Chrome,SongURL: str,tabNo: int):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"DownloaderTrackPage_Form_Input___F7u_")))
    FillBox = DRV.find_element(By.CLASS_NAME,"DownloaderTrackPage_Form_Input___F7u_")
    FillBox.send_keys(SongURL)
    SearchButton = DRV.find_element(By.XPATH,"//button[text() = 'Search']")
    SearchButton.click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"Button_Button__qiii_")))
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"Button_Button__qiii_"))).click()
    time.sleep(2)
    DRV.execute_script("window.open('{0}', '_blank');".format("https://www.soundloaders.com/spotify-downloader/"))
    DRV.switch_to.window(DRV.window_handles[tabNo])
    

if __name__ == "__main__":
    main()
