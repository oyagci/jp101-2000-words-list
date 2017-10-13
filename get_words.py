import selenium
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

myUsername = ''
myPassword = ''

if myUsername == '' or myPassword == '':
    print('Please fill in credentials')
    print('Exiting')
    exit()

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def get_nb_pages(url):
    print('Getting number of pages')
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main_all_2")))
    pagination_links = driver.find_elements_by_class_name('ill-wlv_pagination-a__link')
    nb_pages = 1
    for p in pagination_links:
        nb = safe_cast(p.text, int)
        if nb is not None and nb > nb_pages:
            nb_pages = nb
    print('Number of pages: ' + str(nb_pages))
    return nb_pages

print('Starting geckodriver')
driver = webdriver.Firefox()

print('Loading jp101.com')
driver.get('https://www.japanesepod101.com/')

print('Waiting for the page to be loaded')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "_atssh")))

print('Loging in')
driver.find_element_by_class_name('r101-sign-in--a__button').click()
username = driver.find_element_by_name('amember_login')
password = driver.find_element_by_name('amember_pass')

username.send_keys(myUsername)
password.send_keys(myPassword)

driver.find_element_by_class_name('r101-sign-in--a__submit').click()

print('Waiting for login')
wait = WebDriverWait(driver, 30)
element = wait.until(EC.title_is('Redirect'))

print('Start processing words')
core_words = [100, 200, 300, 400, 500, 600, 700, 900, 1000, 2000]
words_data = []
aindex = 0
for core_word in core_words:
    aindex += 1
    nb_pages = get_nb_pages('https://www.japanesepod101.com/japanese-word-lists/?coreX=' + str(core_word))
    print('Processing core words ' + str(core_word) + ' for ' + str(nb_pages) + ' pages ')
    bindex = 0
    for nb in range(1, nb_pages + 1):
        bindex += 1
        print("Page " + str(bindex))
        driver.get('https://www.japanesepod101.com/japanese-word-lists/?coreX=' + str(core_word) + '&page=' + str(nb))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "main_all_2")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        scripts = soup.findAll('script')
        file = open('data_' + str(aindex) + '_' + str(bindex) + '.json', 'w')
        for script in scripts:
            lines = str(script).split('\n')
            for line in lines:
                if 'words =' in line:
                    data = line[10:-1]
                    json_data = json.loads(data)
                    dumps = json.dumps(json_data, sort_keys=False, indent=4)
                    file.write(dumps)
        file.close()
