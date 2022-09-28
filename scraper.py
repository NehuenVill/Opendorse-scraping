from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

api_base_url = 'https://api.opendorse.com'

def get_athletes():

    url = f"{api_base_url}/marketplaces/search/athlete-search"

    payload = {
        "pageNumber": 1,
        "pageSize": 200000,
        "orderBy": "DealsCompleted",
        "showAthletesWithoutDeals": False,
        "showUnclaimedAccounts": False
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    all_athletes = response.json()

    count = 0
    file_num = 0

    for athlete in all_athletes['data']['data']:

        if count > 20_000:

            file_num += 1
            count = 0

        print(athlete['networkProfileCode'])
        print('')

        with open(f'Athletes_code({file_num}).json') as f:

            data = json.load(f)

        with open(f'Athletes_code({file_num}).json', 'w') as f:

            data['Codes'].append(athlete['networkProfileCode'])

            json.dump(data, f, indent=2)

        count += 1

def get_profiles_info(base_url : str, codes : list):

    driver = webdriver.Chrome()

    driver.get(base_url)

    for code in codes:

        main_window = driver.current_window_handle
  
        driver.execute_script("window.open(arguments[0], 'secondtab');", f'{base_url}profile/{code}')

        split_patern = '•'

        title_path = 'div/h3'

        # Getting the information about the athletes

        # Reminder: To retrieve all the information possible loop through all the info items,
        # then check if the title of the field fits the field you're analizing by changing the 
        # last part of the element's xpath. This way the program will be able to work with all
        # kind of profiles, from complete ones to totally incomplete ones.
        # Then save all the information in json.

        name = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div[1]/div[1]/div[1]/span/h1/div[1]').text

        twiter_followers = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/a[1]/div/p').text

        instagram_followers = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/a[2]/div/p').text

        afiliations_list = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[2]/div/p').text.split(split_patern)

        afiliations = ''

        for afiliation in afiliations_list:

            afiliations += f'{afiliation}, '

        accolades_list = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[3]/div/p').text.split(split_patern)

        accolades = ''

        for accolade in accolades_list:

            accolades += f'{accolade}, '

        bg_list = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[5]/div/p').text.split(split_patern)

        bg = ''

        for item in bg_list:

            bg += f'{item}, '

        location = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[4]/div/p').text

        hometown = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[6]/div/p').text


if __name__ == '__main__':

    get_athletes()
    get_profiles_info('https://opendorse.com/')