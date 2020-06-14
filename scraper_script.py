from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'http://sante.gouv.qc.ca/en/repertoire-ressources/votre-cisss-ciusss/'

# get postal codes
postal_codes = []
f = open('postal_codes.txt', 'r')
for code in f.readlines():
    postal_codes.append(code.strip())
f.close()

# remove any new lines
for i in range(len(postal_codes)):
    if postal_codes[i] == "":
        postal_codes[i].pop()

# at this point data is cleaned

############ Scraping Script ###############

health_regions = []

# build browser
browser = webdriver.Firefox()
for code in postal_codes:
    browser.get(link)

    # flll text box with postal code
    formElem = browser.find_element_by_id("codePostal")
    formElem.send_keys(code)

    # click submit link
    submitElem = browser.find_element_by_id("bt_rechCode")
    submitElem.click()

    # wait 15 sec
    try:
        element = WebDriverWait(browser, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bande_foncer"))
        )
    except:
        health_regions.append(" ")
        continue
    # save resulting text

    try:
        targetElem = browser.find_element_by_class_name("bande_foncer")
        health_regions.append(targetElem.text)
    except selenium.common.exceptions.StaleElementReferenceException:
        health_regions.append(" ")

########### build csv ########
f_new = open('post_w_regions.csv', 'w')
for i, j in zip(postal_codes, health_regions):
    f_new.write(i + "," + j + "\n")

f_new.close()
