import time

import psutil
import requests
from behave import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from termcolor import colored

from etp_client.Utils.ClientUtilClass import ClientUtil

# Documentation
# This test suite is for validating client's performance, and that we don't break the internet
# The test:
#       1) navigate to sites one after the other,
#       2) check performance statistics such as PLT and TTFB
#       3)  print errors in the browser
#       4) compare performance statistics with and without client
# flow: we are in protected mode
#       test starts (navigating to sites)
#       1 minute sleep time for disabling the client manually
#       test continues (navigating to sites)
#       test concludes , statistics + average are printed

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


def selecting_alexa_sites():
    baseUrl = "http://www."
    alexaSites = [
        baseUrl + "google.com",
        baseUrl + "youtube.com",
        baseUrl + "facebook.com",
        baseUrl + "baidu.com",
        baseUrl + "wikipedia.org",
        baseUrl + "yahoo.com",
        baseUrl + "qq.com",
        baseUrl + "taobao.com",
        baseUrl + "tmall.com",
        baseUrl + "sohu.com",
        baseUrl + "amazon.com",
        baseUrl + "live.com",
        baseUrl + "vk.com",
        baseUrl + "twitter.com",
        baseUrl + "reddit.com",
        baseUrl + "instagram.com",
        baseUrl + "sina.com",
        baseUrl + "360.cn",
        baseUrl + "linkedin.com",
        baseUrl + "jd.com",
        baseUrl + "weibo.com",
        baseUrl + "yahoo.co",
        baseUrl + "hao123.com",
        baseUrl + "ntd.tv",
        baseUrl + "yandex.ru",
        baseUrl + "ebay.com",
        baseUrl + "4chan.org.",
        baseUrl + "msn.com",
        baseUrl + "homedepot.com",
        baseUrl + "wordpress.com",
        baseUrl + "bing.com",
        baseUrl + "netflix.com",
        baseUrl + "ok.ru",
        baseUrl + "aliexpress.com",
        baseUrl + "tutorialspoint.com",
        baseUrl + "list.tmall",
        baseUrl + "microsoft.com",
        baseUrl + "blogspot.com",
        baseUrl + "imgur.com",
        baseUrl + "stackoverflow.com",
        baseUrl + "imdb.com",
        baseUrl + "office.com",
        baseUrl + "ign.com",
        baseUrl + "tianya.cn",
        baseUrl + "diply.com",
        baseUrl + "apple.com",
        baseUrl + "dell.com",
        baseUrl + "twitch.tv",
        baseUrl + "github.com",
        baseUrl + "csdn.net",
        baseUrl + "mail.ru",
        baseUrl + "target.com",
        baseUrl + "alipay.com",
        baseUrl + "pinterest.com",
        baseUrl + "paypal.com",
        baseUrl + "wikia.com",
        baseUrl + "atlassian.net.",
        baseUrl + "adobe.com",
        baseUrl + "alibaba.com",
        baseUrl + "bbc.com.",
        baseUrl + "dropbox.com",
        baseUrl + "askcom.com",
        baseUrl + "stackexchange.com",
        baseUrl + "amazon.de",
        baseUrl + "webmd.com.",
        baseUrl + "salesforce.com",
        baseUrl + "theguardian.com.",
        baseUrl + "theverge.com.",
        baseUrl + "ettoday.net.",
        baseUrl + "huffingtonpost.com.",
        baseUrl + "udemy.com.",
        baseUrl + "trello.com.",
        baseUrl + "chase.com.",
        baseUrl + "steampowered.com.",
        baseUrl + "cnet.com.",
        baseUrl + "outbrain.com.",
        baseUrl + "9gag.com.",
        baseUrl + "indeed.com.",
        baseUrl + "vice.com.",
        baseUrl + "mediafire.com.",
        baseUrl + "uber.com.",
        baseUrl + "xda-developers.com.",
        baseUrl + "bp.blogspot.com.",
        baseUrl + "playstation.com.",
        baseUrl + "slack.com.",
        baseUrl + "github.io.",
        baseUrl + "howtogeek.com.",
        baseUrl + "coursera.org.",
        baseUrl + "java.com.",
        baseUrl + "glassdoor.com.",
        baseUrl + "nbcnews.com.",
        baseUrl + "rottentomatoes.com.",
        baseUrl + "investing.com.",
        baseUrl + "washingtonpost.com.",
        baseUrl + "w3schools.com.",
        baseUrl + "gsmarena.com.",
        baseUrl + "cbsnews.com.",
        baseUrl + "google.be.",
        baseUrl + "nba.com.",
        baseUrl + "hp.com.",
        baseUrl + "oracle.com.",
        baseUrl + "ameblo.jp.",
        baseUrl + "blogspot.in.",
        baseUrl + "nih.gov.",
        baseUrl + "telegraph.co.uk.",
        baseUrl + "samsung.com.",
        baseUrl + "wikihow.com.",
        baseUrl + "shutterstock.com.",
        baseUrl + "godaddy.com.",
        baseUrl + "steamcommunity.com.",
        baseUrl + "bankofamerica.com.",
        baseUrl + "spotify.com.",
        baseUrl + "mercadolivre.com.br.",
        baseUrl + "livejournal.com.",
        baseUrl + "cnbc.com.",
        baseUrl + "ozock.com.",
        baseUrl + "forbes.com.",
        baseUrl + "zillow.com",
        baseUrl + "weather.com.",
        baseUrl + "wsj.com.",
        baseUrl + "tistory.com.",
        baseUrl + "marketwatch.com.",
        baseUrl + "goo.ne.jp.",
        baseUrl + "redtube.com.",
        baseUrl + "foxnews.com.",
        baseUrl + "apache.org.",
        baseUrl + "southwest.com.",
        baseUrl + "verizon.com.",
        baseUrl + "cloudflare.com.",
        baseUrl + "skype.com.",
        baseUrl + "mozilla.org."

    ]
    return alexaSites


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
        print_errors_from_console_log(driver)
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


def print_errors_from_console_log(driver):
    try:
        for log_entry in driver.get_log('browser'):
            if log_entry["level"] == "SEVERE" and 'Failed to load resource' in log_entry['message']:
                print(colored(log_entry, 'red'))
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


def step_impl(context):
    sleep_time = 15
    print(
        "*** *** *** ***              sleeping to allow disabling  for %s seconds               *** *** *** ***" % sleep_time)
    time.sleep(sleep_time)


@then("checking the client is not adding 5ms and closing the browser")
def step_impl(context):
    driver.quit()
    for key in web_statistics_with_client_first_run.keys():
        assert (web_statistics_with_client_first_run[key] * 1000 - web_statistics_without_client_second_run[
            key] * 1000 > 5)
        assert False, 'increase is more then 5ms for these sites: key: {}'.format(key)


@then("client will be enabled")
def step_imple(conetext):
    ClientUtil.client_restart()
    time.sleep(20)
