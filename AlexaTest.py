import random
import string
import time

import psutil
import requests
from behave import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from termcolor import colored

from etp_client.Utils.ClientUtilClass import ClientUtil



use_step_matcher("re")

# support options such as incognito
options = webdriver.ChromeOptions()
# options.add_argument("--incognito")
options.add_argument("--headless")

# support browser log
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(options=options, desired_capabilities=d)
web_statistics_with_client_first_run = {}
web_statistics_without_client_second_run = {}


@given("etp-client is installed and enabled")
def step_impl(context):
    print("client is enabled")


@when("browsing to the websites, and it's the first run - client should be enabled")
def step_impl(context):
    sites = selecting_alexa_sites()
    navigate_to_site(sites, web_statistics_with_client_first_run)


@when("browsing to the websites, and it's the second run - client should be disabled")
def step_impl(context):
    sites = selecting_alexa_sites()
    navigate_to_site(sites, web_statistics_without_client_second_run)
    get_average_statistics()


@then("the user reach the websites as expected in reasonable time")
def step_impl(context):
    for key in web_statistics_with_client_first_run.keys():
        print('navigation time with client - key: {}, value: {}'.format(key, web_statistics_with_client_first_run[key]))
        print('navigation time without client - key: {}, value: {}'.format(key,
                                                                           web_statistics_without_client_second_run[
                                                                               key]))


def selecting_alexa_sites(iterations):
    site_list = ["google.com", "youtube.com", "facebook.com", "wikipedia.org", "yahoo.com", "amazon.com",
                 "live.com", "vk.com", "twitter.com", "reddit.com", "foxnews.com", "apache.org", "southwest.com",
                 "cloudflare.com", "instagram.com", "linkedin.com", "yahoo.co", "ameblo.jp", "verizon.com",
                 "udemy.com", "target.com", "imgur.com", "yandex.ru", "ebay.com", "4chan.org", "msn.com",
                 "homedepot.com", "wordpress.com", "bing.com", "netflix.com", "ok.ru", "aliexpress.com",
                 "tutorialspoint.com", "list.tmall.com", "microsoft.com", "blogspot.com", "stackoverflow.com",
                 "imdb.com", "office.com", "ign.com", "diply.com", "weather.com", "wsj.com", "marketwatch.com",
                 "goo.ne.jp", "apple.com", "dell.com", "twitch.tv", "github.com", "csdn.net", "mail.ru",
                 "alipay.com", "pinterest.com", "paypal.com", "wikia.com", "atlassian.net", "adobe.com",
                 "alibaba.com", "livejournal.com", "cnbc.com", "forbes.com", "zillow.com",
                 "bbc.com", "dropbox.com", "stackexchange.com", "amazon.de", "webmd.com", "salesforce.com",
                 "theguardian.com", "theverge.com", "ettoday.net", "huffingtonpost.com", "trello.com", "chase.com",
                 "steampowered.com", "cnet.com", "outbrain.com", "9gag.com", "indeed.com", "vice.com",
                 "mediafire.com", "uber.com", "xda-developers.com", "mozilla.org", "playstation.com", "slack.com",
                 "github.io", "howtogeek.com", "coursera.org", "java.com", "glassdoor.com", "nbcnews.com",
                 "rottentomatoes.com", "investing.com", "washingtonpost.com", "w3schools.com", "gsmarena.com",
                 "cbsnews.com", "google.be", "nba.com", "hp.com", "spotify.com", "oracle.com", "nih.gov",
                 "telegraph.co.uk", "samsung.com", "wikihow.com", "skype.com", "shutterstock.com", "godaddy.com",
                 "steamcommunity.com", "bankofamerica.com"]

    baseUrl = "https://www."

    new_list = []
    for i in range(iterations):
        for site in site_list:
            new_list.append(baseUrl + site)

    return new_list


def navigate_to_site(sites, results):
    number_of_sites = len(sites)
    counter = 1
    for site in sites:
        print("about to navigate to: " + site)
        print(f"site number {counter} / {number_of_sites}")
        counter = counter + 1
        # response code function only supported when client is disabled
        # get_response_code(site)
        driver.get(site)
        (ttfb, plt) = web_statistics(driver)
        print_errors_from_console_log(driver, site)
        results[site + '_TTFB'] = ttfb
        results[site + '_PLT'] = plt


def web_statistics(driver):
    # print cpu and memory stats
    print(colored("CPU: ", 'blue'))
    print(psutil.cpu_times_percent(interval=1, percpu=False))
    print(colored("MEMORY: ", 'blue'))
    print(psutil.virtual_memory())

    """ Use Navigation Timing  API to calculate the timings that matter the most """
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")

    ''' Calculate the performance'''
    backendPerformance_calc = (responseStart - navigationStart) / 1000
    frontendPerformance_calc = (domComplete - responseStart) / 1000

    print(colored("TTFB = Time to first byte in seconds: %s", 'green') % backendPerformance_calc)
    print(colored("PLT = Page loading time in seconds: %s", 'green') % frontendPerformance_calc)

    return (backendPerformance_calc, frontendPerformance_calc)


def print_errors_from_console_log(driver, website_name=None):
    try:
        for log_entry in driver.get_log('browser'):
            if log_entry["level"] == "SEVERE" and 'Failed to load resource' in log_entry['message']:
                print(colored(log_entry, 'red'))
                if 'status of' in log_entry['message']:
                    print("saving screenshot for site: "+website_name)
                    print(randomString()+".png")
                    driver.save_screenshot(randomString()+".png")
    except Exception as e:
        print("Exception when reading browser log")
        print(str(e))


def get_response_code(site):
    try:
        r = requests.get(site)
        print("HTTP status code: " + str(r.status_code))
    except requests.ConnectionError:
        print("failed to connect")


def get_average_statistics():
    # calc for with client
    total_time_TTFB_with_client = 0
    total_time_PLT_with_client = 0
    total_number_of_sites = len(web_statistics_with_client_first_run)
    for key in web_statistics_with_client_first_run.keys():
        if "TTFB" in key:
            total_time_TTFB_with_client = total_time_TTFB_with_client + web_statistics_with_client_first_run[key]
        elif "PLT" in key:
            total_time_PLT_with_client = total_time_PLT_with_client + web_statistics_with_client_first_run[key]

    print('navigation time with client TTFB average is %s seconds' % (
            total_time_TTFB_with_client / (total_number_of_sites / 2)))
    print('navigation time with client PLT average is %s seconds' % (
            total_time_PLT_with_client / (total_number_of_sites / 2)))

    # calc for without client
    total_time_TTFB_without_client = 0
    total_time_PLT_without_client = 0
    for key in web_statistics_without_client_second_run.keys():
        if "TTFB" in key:
            total_time_TTFB_without_client = total_time_TTFB_without_client + web_statistics_without_client_second_run[
                key]
        elif "PLT" in key:
            total_time_PLT_without_client = total_time_PLT_without_client + web_statistics_without_client_second_run[
                key]

    print('navigation time without client TTFB average is %s seconds' % (
            total_time_TTFB_without_client / (total_number_of_sites / 2)))
    print('navigation time without client PLT average is %s seconds' % (
            total_time_PLT_without_client / (total_number_of_sites / 2)))


@given("etp-client is disabled")
def step_impl(context):
    ClientUtil.disable_etp_client()
    sleep_time = 15
    print(
        "*** *** *** ***              sleeping to allow disabling client for %s seconds               *** *** *** ***" % sleep_time)
    time.sleep(sleep_time)


@then("checking the client is not adding 5ms and closing the browser")
def step_impl(context):
    driver.quit()
    for key in web_statistics_with_client_first_run.keys():
        assert (web_statistics_with_client_first_run[key] * 1000 - web_statistics_without_client_second_run[
            key] * 1000 > 5)
        assert False, 'etp client increase is more then 5ms for these sites: key: {}'.format(key)


@then("client will be enabled")
def step_imple(context):
    ClientUtil.client_restart()
    time.sleep(20)

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

