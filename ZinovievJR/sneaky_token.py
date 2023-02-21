# see rkengler.com for related blog post
# https://www.rkengler.com/how-to-capture-network-traffic-when-scraping-with-selenium-and-python/

import json
import pprint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+



def process_browser_logs_for_network_events():
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    driver = webdriver.Chrome(
    desired_capabilities=capabilities,
)

    driver.get("https://glossary.slb.com/en/search")

    logs = driver.get_log("performance")
    logs_for_log =[]
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            logs_for_log.append(log)

    jsonString = json.dumps(logs_for_log)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    driver.close()
    return logs_for_log

def get_header():
    fileObject = open("data.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)
    for i in aList:
        try:
            if i['params']['headers']['authorization']:
                header = i['params']['headers']
                return dict(list(header.items())[4:])
        except KeyError:
            pass
    fileObject.close()










