import psutil
from selenium import webdriver
from termcolor import colored

from dyno.core.logger import Logger
from etp_client.flows.Alexa.steps.AlexaTest import print_errors_from_console_log, web_statistics

logger = Logger(__name__)


class SeleniumBrowsers:

    @classmethod
    def createBrowser(cls, url, browser='chrome', expectedText=None, headless=True, incognito=False):
        driver = cls.selectBrowser(browser)
        print("about to navigate to: " + url)
        driver.get(url)
        web_statistics(driver)
        print_errors_from_console_log(driver)
        if expectedText:
            assert (expectedText in driver.page_source)
        driver.close()

    @classmethod
    def selectBrowser(cls, browser):
        if browser == 'chrome':
            print("selected Chrome browser")
            return webdriver.Chrome()
        elif browser == 'firefox':
            print("selected Firefox browser")
            return webdriver.Firefox()
        elif browser == 'safari':
            print("selected Safari browser")
            return webdriver.Safari()

    @classmethod
    def createBrowserHeadlessParallel(cls, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        print("about to navigate to: " + url)
        driver.get(url)
        print_errors_from_console_log(driver)
        web_statistics(driver)
        driver.close()

    @classmethod
    def print_cpu_stats(cls):
        print(colored("CPU: ", 'blue'))
        print(psutil.cpu_times_percent(interval=1, percpu=False))

    @classmethod
    def print_memory_stats(cls):
        print(colored("MEMORY: ", 'blue'))
        print(psutil.virtual_memory())
