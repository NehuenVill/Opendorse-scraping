from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import json
import pandas as pd

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

    bio_path = ['/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div[2]', '/html/body/div[1]/main/div[3]/div/div[1]/div[3]/div/div[1]/div/div[2]']

    split_patern = '•'

    field_info = ''

    for i in range(6):

        try:
            title = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[{i+1}]/div/div[1]/h3').text
                                                            
        except Exception:

            try:
                title = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div/div[1]/div[3]/div/div[{i+1}]/div/div[1]/h3').text

            except Exception as e:

                print(e)
                continue

        if title == 'Biography' and field == 'Biography':
            
            try:

                info = driver.find_element(By.XPATH, bio_path[0]).text.replace('\n', '- ')

            except Exception:

                try:

                    info = driver.find_element(By.XPATH, bio_path[1]).text.replace('\n', '- ')  

                except Exception:

                    info = ''          
            
            field_info = info

            break

        elif title == field:


            try:

                info = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div[2]/div[1]/div[3]/div/div[{i+1}]/div/p').text.split(split_patern)

            except Exception:

                try:
                    
                    info = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[3]/div/div[1]/div[3]/div/div[{i+1}]/div/p').text.split(split_patern)

                except Exception:
                    
                    info = []

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

    chrome_options = Options()
    
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.get(base_url)

    sports_list = ['Football', 'Softball', 'Baseball', 'Marathon',
                   'Fencing', 'Bowling', 'Dance', 'Field Hockey',
                   'Gymnastics', 'Rowing', 'Cheerleading', 'Golf',
                   'Wrestling', 'Ice Hockey', 'Ice Hockey', 'Soccer',
                   'Basketball', 'Rifle', 'Flag Football', 'Beach Volleyball',
                   'Diving', 'Skiing', 'Water Polo', 'Lacrosse',
                   'Tennis', 'Swimming', 'Cross Country',
                   'Volleyball', 'Track & Field']

    count = 0
    file_num = 22

    for code in codes:

        main_window = driver.current_window_handle
  
        driver.execute_script("window.open(arguments[0], 'secondtab');", f'{base_url}profile/{code}')

        driver.switch_to.window("secondtab")
        """
        try: 

            element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-qa='go-home-button']"))
            )

            print(f'this is the element: {element}')

        except Exception as e:

            print(e)

            with open('Errors.json') as f:

                data = json.load(f)

            with open('Errors.json', 'w') as f:

                data['Codes'].append(code)

                json.dump(data, f, indent=4)

                print('')
                print(code)
                print('')

            driver.close()

            driver.switch_to.window(main_window)

            WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

            continue

        """
        try:

            element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@data-qa='go-home-button']"))
                )

            print(f'this is the element: {element}')
        
        except Exception:

            with open('Errors2.json') as f:

                    data = json.load(f)

            with open('Errors2.json', 'w') as f:

                data['Codes'].append(code)

                json.dump(data, f, indent=4)

                print('')
                print(code)
                print('')

                driver.close()

                driver.switch_to.window(main_window)

                WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

                continue

        sleep(1)
        
        try:

            name = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[1]/div[1]/span/h1/div[1]').text
                                            
        except Exception as e:


            try:

                name = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[1]/div[1]/div[1]/span/h1/div[1]').text

            except Exception:

                with open('Errors2.json') as f:

                    data = json.load(f)

                with open('Errors2.json', 'w') as f:

                    data['Codes'].append(code)

                    json.dump(data, f, indent=4)

                    print('')
                    print(code)
                    print('')

                driver.close()

                driver.switch_to.window(main_window)

                WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

                continue
                

        # To find the sport: "p[color='#5a6979']", first element, split by '•' and select first element.
        
        try:

            sport = driver.execute_script("""return document.querySelector("p[color='#5a6979']").textContent""").split(' • ')

            if any(sp in sport[0] for sp in sports_list):

                sport = sport[0]

            else:

                sport = 'Not available'

        except Exception:

            sport = 'Not available'

        bio = find_field(driver, 'Biography')

        afiliations = find_field(driver, 'Affiliations')

        accolades = find_field(driver, 'Accolades')

        bg = find_field(driver, 'Background')

        location = find_field(driver, 'Location')

        hometown = find_field(driver, 'Hometown')

        # Products they offer:

        try:

            shoutout = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/p[2]').text.replace('+', '')
                                                    
            post = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/p[2]').text.replace('+', '')

            appearance = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/p[2]').text.replace('+', '')

            autograph = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/p[2]').text.replace('+', '')

        except Exception as e:

            try:
            
                shoutout = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/p[2]').text.replace('+', '')
                                                        
                post = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/p[2]').text.replace('+', '')

                appearance = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/p[2]').text.replace('+', '')
                                                            
                autograph = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/p[2]').text.replace('+', '')

            except Exception:

                with open('Errors2.json') as f:

                    data = json.load(f)

                with open('Errors2.json', 'w') as f:

                    data['Codes'].append(code)

                    json.dump(data, f, indent=4)

                    print('')
                    print(code)
                    print('')

                    driver.close()

                    driver.switch_to.window(main_window)

                    WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

                    continue

        try:

            pitch_anything = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div[2]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div/p[2]').text.replace('+', '')

        except Exception as e:

            try:

                pitch_anything = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[2]/div[1]/div[2]/div[4]/div/div[2]/div/p[2]').text.replace('+', '')

            except Exception:

                pitch_anything = 'Not available'

        athlete_info = {
            'Name' : name,
            'Sport' : sport,
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

        if count > 1477 and file_num == 22:

            file_num += 1
            count = 0

        if count > 2500:

            file_num += 1
            count = 0

        print(athlete_info)

        with open(f'athletes({file_num}).json') as f:

            data = json.load(f)

        with open(f'athletes({file_num}).json', 'w') as f:

            data['athletes'].append(athlete_info)

            json.dump(data, f, indent=2)

        count += 1

        driver.close()

        driver.switch_to.window(main_window)

        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))

        
def save_output(output):
    
    df = pd.DataFrame(output, columns=['Name', 'Sport', 'Biography',
                                    'Afiliations', 'Accolades', 'Background',
                                    'Location', 'Hometown',
                                    'Shoutout - cost', 'Post - cost',
                                    'Appearance - cost', 'Autograph - cost', 'Pitch anything - cost'])

    df.to_excel("Athletes.xlsx", index=False, columns=['Name', 'Sport', 'Biography',
                                    'Afiliations', 'Accolades', 'Background',
                                    'Location', 'Hometown',
                                    'Shoutout - cost', 'Post - cost',
                                    'Appearance - cost', 'Autograph - cost', 'Pitch anything - cost'])

if __name__ == '__main__':

    """

    athletes_codes = []

    for i in range(1):

        with open(f'Athletes_code({i+3}).json') as f:

            data = json.load(f)

        for ath in data['Codes']:

            athletes_codes.append(ath)


    print(f'number of athletes: {len(athletes_codes)}')

    get_profiles_info('https://opendorse.com/', athletes_codes[323:])

    """

    all_data = []

    for i in range(28):

        with open(f'athletes({i}).json') as f:

            data = json.load(f)['athletes']

            for item in data:

                all_data.append(item)

    print(f'The total amount of items is: {len(all_data)} profiles.')

    save_output(all_data)



"""
if __name__ == '__main__':

    with open(f'Errors.json') as f:

        data = json.load(f)

    print(f"number of athletes: {len(data['Codes'])}")

    get_profiles_info('https://opendorse.com/', data['Codes'][36:])

"""