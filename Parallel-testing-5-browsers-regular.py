from joblib import Parallel, delayed
from etp_client.flows.Alexa.steps.AlexaTest import selecting_alexa_sites
from etp_client.Utils.WebDriverUtil import SeleniumBrowsers

# going to navigate with few browsers to alexa sites, 5 workers, regular
sites = selecting_alexa_sites()
sites2 = ["http://www.google.com", "http://www.ynet.co.il"]

Parallel(n_jobs=5, verbose=10)(delayed(SeleniumBrowsers.createBrowser)(site) for site in sites)
