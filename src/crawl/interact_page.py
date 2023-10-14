import time
import random
from typing import List, Iterator
from contextlib import contextmanager

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from .log import logger, exception


@exception(logger)
@contextmanager
def open_driver(options: Options | None) -> Iterator[WebDriver]:
    try:
        logger.info('Initial Chrome WebDriver')
        driver = uc.Chrome(options=options, headless=False)
        time.sleep(2)
        yield driver
    finally:
        driver.close()


@exception(logger)
def random_wait(wait: int = 5, delta: float = 1) -> float:
    return random.uniform(abs(wait - delta), abs(wait - delta))


@exception(logger)
def check_loaded_page(driver: WebDriver, by: str, value: str, retry: int = 3, wait: float = 5) -> bool:
    count = 0
    while (count < retry):
        try:
            is_appeared = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((by, value)))
            print(is_appeared)
            if is_appeared:
                break
        except:
            driver.refresh()
        count += 1
    logger.info(
        f'Waiting for {driver.current_url} with the {count} trying')
    if count >= retry:
        False
    return True


@exception(logger)
def scroll_end_page(driver: WebDriver, retry: int = 3, wait: float = 8) -> None:
    count = 0
    while (count < retry):
        logger.info(f'Scrolling {driver.current_url} to the end')
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(wait)
        count += 1


@exception(logger)
def get_element(driver: WebDriver | WebElement, by: str, value: str) -> WebElement | None:
    logger.info(f'Getting a element by "{by}" with "{value}" value')
    elements = driver.find_elements(by=by, value=value)
    if len(elements) > 0:
        return elements[0]
    return None


@exception(logger)
def get_elements(driver: WebDriver | WebElement, by: str, value: str) -> List[WebElement] | []:
    logger.info(f'Getting a list of element by "{by}" with "{value}" value')
    elements = driver.find_elements(by=by, value=value)
    if len(elements):
        return elements
    return []
