import requests
from bs4 import BeautifulSoup
import json
from proxy_config import login, password, proxy
import csv
from _datetime import datetime

cookies = {
    '_gid': 'GA1.2.1628284846.1685043552',
    'nmstat': 'ca1a7c87-e9a7-aabd-e703-c9772493737d',
    '_ga': 'GA1.1.605199279.1685043551',
    '_ga_WFFDEGRMJE': 'GS1.1.1685114852.2.1.1685115227.0.0.0',
}

headers = {
    'authority': 'www.bls.gov',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_gid=GA1.2.1628284846.1685043552; nmstat=ca1a7c87-e9a7-aabd-e703-c9772493737d; _ga=GA1.1.605199279.1685043551; _ga_WFFDEGRMJE=GS1.1.1685114852.2.1.1685115227.0.0.0',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

proxies = {
    'https': f'http://{login}:{password}@{proxy}'
}

def getData(url):
    cur_date = datetime.now().strftime('%m_%d_%Y')
    # response = requests.get(
    #     'https://www.bls.gov/regions/midwest/data/AverageEnergyPrices_SelectedAreas_Table.htm',
    #     cookies=cookies,
    #     headers=headers,
    #     proxies=proxies
    # )
    # print(response)

    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('table', id='ro5xgenergy')
    data_th = table.find('thead').find_all('tr')[-1].find_all('th')

    table_headers = ['Area']
    for dth in data_th:
        dth = dth.text.strip()
        #print(dth)
        table_headers.append(dth)

    with open(f'data_{cur_date}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                table_headers
            )
        )

    tbody_trs = table.find('tbody').find_all('tr')

    data = []
    for tr in tbody_trs:
        area = tr.find('th').text.strip()

        data_by_month = tr.find_all('td')
        data = [area]
        for dbm in data_by_month:
            if dbm.find('a'):
                area_data = dbm.find('a').get('href')
            elif dbm.find('span'):
                area_data = dbm.find('span').text.strip()
            else:
                area_data = 'None'
            data.append(area_data)
        with open(f'data_{cur_date}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    data
                )
            )
    return 'Work done!'

def main():
    print(getData('https://www.bls.gov/regions/midwest/data/AverageEnergyPrices_SelectedAreas_Table.htm'))

if __name__ == '__main__':
    main()