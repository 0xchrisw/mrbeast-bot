#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import sys; sys.dont_write_bytecode = True;

import warnings
import random
import requests
import re

from datetime import datetime, time
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

warnings.filterwarnings("ignore", category=DeprecationWarning)


mrbeast_yt_profile = "https://www.youtube.com/user/MrBeast6000"
mrbeast_yt_uploads = f"{mrbeast_yt_profile}/videos"
mrbeast_last_upload   = "dZklZVaU4AI"
mrbeast_target_upload = None

target_time = datetime(2022, 8, 4, 15, 45, 0)


def get_mrbeast_last_upload():
    r = requests.get(mrbeast_yt_uploads)
    if r.status_code == 200:
      html = r.text
      return re.search('(?<="videoId":").*?(?=")', html).group()
    else:
      return None


while (target_time > datetime.now()):
  print(f"Starting in {target_time - datetime.now()}")
  sleep(1)


while (mrbeast_target_upload := get_mrbeast_last_upload()) and \
       mrbeast_last_upload == mrbeast_target_upload:
  print(f"Waiting for new uploads...")
  sleep(1)


class ShoopDaWhoop:
  def __init__(self):
    self.profile = self.get_profile()
    self.driver  = self.create_driver()

  # Get the user's Firefox profile.
  def get_profile(self):
    mozille_home = Path.home() / ".mozilla/firefox"
    user_profile = None
    if not mozille_home.exists(): exit()
    _profiles = [d for d in mozille_home.iterdir() if d.is_dir() and '.default' in d.name]
    for profile in _profiles:
      if (profile / "settings").exists():
        user_profile = profile
        break
    print(f"Using profile: {user_profile}")
    return user_profile

  # Create the webdriver.
  def create_driver(self):
    options = Options()
    options.page_load_strategy = 'normal'

    profile = webdriver.FirefoxProfile(self.profile)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
    driver = webdriver.Firefox(
      options = options,
      firefox_profile=profile,
      desired_capabilities=desired
    )
    return driver

  # Load the video URL and leave a comment!
  def firin_mah_lazer(self, url):
    driver = self.driver
    print(f"Firing {url}")
    driver.get(url)
    driver.implicitly_wait(1)
    # Scroll down a bit
    driver.execute_script("window.scrollTo(0, 1000);")
    # ... a bit more.
    html_element = WebDriverWait(driver=driver, timeout=9).until(
      EC.presence_of_element_located((By.ID, "meta"))
    )
    _action = ActionChains(driver)
    _meta = driver.find_element(By.ID, "meta")
    _action.click().send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()
    sleep(1)
    _action.click().send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()
    # Find the Comment box
    html_element = WebDriverWait(driver=driver, timeout=9).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-simplebox-renderer"))
    )
    _action = ActionChains(driver)

    driver.find_element(By.ID, "placeholder-area").click()
    driver.find_element(By.ID, "contenteditable-root").send_keys("First!")

    driver.find_element(By.ID, "submit-button").click()
    print("Fired!")

  def open_new_window(self, url):
    driver.execute_script(f"window.open('{url}')")
    driver.switch_to.window(driver.window_handles[-1])

  # Close all windows related to driver instance.
  def exit(self):
    return self.driver.quit()


Cannon = ShoopDaWhoop()
Cannon.firin_mah_lazer(f"https://www.youtube.com/watch?v={mrbeast_target_upload}")
Cannon.exit()