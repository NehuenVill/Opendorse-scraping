from selenium import webdriver
import requests
import json

base_url = 'https://api.opendorse.com'

def get_athletes():

    url = f"{base_url}/marketplaces/search/athlete-search"

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



if __name__ == '__main__':

    get_athletes()
