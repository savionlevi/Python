from joblib import Parallel, delayed
from etp_client.flows.Alexa.steps.AlexaTest import selecting_alexa_sites
from etp_client.Utils.WebDriverUtil import SeleniumBrowsers

# going to navigate with few browsers to alexa sites, 15 workers, headless
sites = selecting_alexa_sites()
sites2 = ["http://www.google.com", "http://www.ynet.co.il"]

Parallel(n_jobs=20, verbose=10)(delayed(SeleniumBrowsers.createBrowserHeadlessParallel)(site) for site in sites)

#example of output (test summary):
#[Parallel(n_jobs=15)]: Using backend LokyBackend with 15 concurrent workers.
#about to navigate to: ...
#TTFB = Time to first byte in seconds:
#PLT = Page loading time in seconds
#[Parallel(n_jobs=15)]: Done   2 tasks      | elapsed:   19.4s
#[Parallel(n_jobs=15)]: Done  11 tasks      | elapsed:   38.9s