from behave import *
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

use_step_matcher("re")

options = webdriver.FirefoxOptions()
options.add_argument("--incognito")

d = DesiredCapabilities.FIREFOX
d['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Firefox(options=options)


###scenario 1 - IP site###
@when("Navigating to IP successfully")
def step_impl(context):
    driver.get("http://17.178.96.59/")
    page_is_loaded("iPhone")


@then("browsing is successful")
def step_impl(context):
    print("success")

    ###scenario 2 - geolocation###


@when("Navigating to geolocation checker")
def step_impl(context):
    driver.get("https://mylocation.org/")
    print("success")


@then("country is as expected")
def step_impl(context):
    page_is_loaded("Israel")
    print("success")

    ###scenario 3 - long url###


@when("navigating to long url")
def step_impl(context):
    driver.get(
        "http://thelongestlistofthelongeststuffatthelongestdomainnameatlonglast.com"
        "/wearejustdoingthistobestupidnowsincethiscangoonforeverandeverandeverbutitstilllookskindaneatinthebrowsereventhoughitsabigwasteoftimeandenergyandhasnorealpointbutwehadtodoitanyways.html")
    print("success")


@then("page is shown as expected")
def step_impl(context):
    page_is_loaded("Longest")
    print("success")

    ###scenario 4 - web servers###


@when("navigating to common web servers")
def step_impl(context):
    sites = create_web_server_list()
    site_validation = ["DuckDuckGo", "Microsoft", "Bai"]
    for counter, site in enumerate(sites):
        driver.get(site)
        page_is_loaded(site_validation[counter])
    print("success")


@then("navigation is successful")
def step_impl(context):
    print("success")
    driver.quit()


def page_is_loaded(text):
    assert (text in driver.page_source)


def create_web_server_list():
    base_url = "https://www."
    web_server_list = [
                       base_url+"duckduckgo.com",  # nginx
                       base_url+"office.com",  # IIS
                       base_url+"baidu.com"  # apache
                       ]
    return web_server_list
