from behave import *
from self import self
from etp_client.Utils.WebDriverUtil import SeleniumBrowsers

use_step_matcher("re")


###scenario 1 - IP site###
@when("Navigating using Chrome , Firefox, Safari browsers successfully")
def step_impl(context):
    #chrome
    navigate_to_sites(create_site_dictionary(), 'chrome')

    #Firefox
    navigate_to_sites(create_site_dictionary(), 'firefox')


    # Safari test suite
    navigate_to_sites(create_site_dictionary(), 'safari')


@then("browsing with browsers is successful")
def step_impl(context):
    print("success")


def create_site_dictionary():
    sites = {
        "https://www.akamaietpcnctest.com/": "Dogfooding",
        "http://17.178.96.59/": "iPhone",
        "https://www.nytimes.com/": "times",
        "https://www.edition.cnn.com/": "cnn",
        "https://www.forbes.com/": "Forbes",
        "https://mylocation.org/": "Israel",
        "http://thelongestlistofthelongeststuffatthelongestdomainnameatlonglast.com"
        "/wearejustdoingthistobestupidnowsincethiscangoonforeverandeverandeverbutitstilllookskindaneatinthebrowsereventhoughitsabigwasteoftimeandenergyandhasnorealpointbutwehadtodoitanyways.html": "Longest",
        "https://duckduckgo.com": "DuckDuckGo",
        "https://office.com": "Microsoft",
        "https://baidu.com": "Bai"
    }
    return sites


def navigate_to_sites(site_dictionary, browser):
    for site in site_dictionary:
        SeleniumBrowsers.print_cpu_stats()
        SeleniumBrowsers.print_memory_stats()
        self.browser = SeleniumBrowsers.createBrowser(site, browser, site_dictionary[site])

