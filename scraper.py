from gettext import find
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


def find_field(driver, field):

    bio_path = '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div[2]'

    split_patern = '•'

    field_info = ''

    for i in range(6):

        try:
            title = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[{i+1}]/div/div[1]/h3').text
        except Exception as e:

            print(e)
            continue

        if title == 'Biography' and field == 'Biography':

            info = driver.find_element(By.XPATH, bio_path).text.replace('\n', '- ')

            field_info = info

            break

        elif title == field:

            info = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[{i+1}]/div/p').text.split(split_patern)

            for item in info:

                field_info += f'{item}, '

            break

        else:

            continue

    if field_info:

        return field_info

    else:

        return 'Not available'



def get_profiles_info(base_url : str, codes : list):

    driver = webdriver.Chrome()

    driver.get(base_url)

    for code in codes:

        main_window = driver.current_window_handle
  
        driver.execute_script("window.open(arguments[0], 'secondtab');", f'{base_url}profile/{code}')

        driver.switch_to.window("secondtab")

        element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div[1]/div[1]/div[1]/span/h1/div[1]'))
            )

        name = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div[1]/div[1]/div[1]/span/h1/div[1]').text

        try:

            twitter_followers = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/a[1]/div/p').text

        except Exception as e:

            print(e)

            twiter_followers = 'Not available'

        try:

            instagram_followers = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/a[2]/div/p').text

        except Exception as e:

            print(e)

            instagram_followers = 'Not available'

        bio = find_field(driver, 'Biography')

        afiliations = find_field(driver, 'Affiliations')

        accolades = find_field(driver, 'Accolades')

        bg = find_field(driver, 'Background')

        location = find_field(driver, 'Location')

        hometown = find_field(driver, 'Hometown')

        # Products they offer:

        shoutout = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/p[2]').replace('+', '')

        post = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/p[2]').replace('+', '')

        appearance = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/p[2]').replace('+', '')

        autograph = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/p[2]').replace('+', '')
        
        try:

            pitch_anything = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div/p[2]').replace('+', '')

        except Exception as e:

            print(e)

            pitch_anything = 'Not available'

        athlete_info = {
            'Name' : name,
            'Twitter followers' : twitter_followers,
            'Instagram followers' : instagram_followers,
            'Biography' : bio,
            'Afiliations' : afiliations,
            'Accolades' : accolades,
            'Background' : bg,
            'Location' : location,
            'Hometown' : hometown,
            'Shoutout - cost' : shoutout,
            'Post - cost' : post,
            'Appearance - cost' : appearance,
            'Autograph - cost' : autograph,
            'Pitch anything - cost' : pitch_anything 
        }

        with open('athletes.json') as f:

            data = json.load(f)

        with open('athletes.json', 'w') as f:

            data['athletes'].append(athlete_info)

        driver.close()

        driver.switch_to.window(main_window)

        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

        



if __name__ == '__main__':

    get_profiles_info('https://opendorse.com/')