from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

url  = 'https://www.cars24.com/buy-used-honda-cars-delhi-ncr/'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')

Cars_dict = {}
cars_no = 0
no_page = 1

tables = soup.find_all("div", {"class": "col-sm-12 col-md-6 col-lg-4"})

while cars_no < 40:
    for table in tables:

        url = 'https://www.cars24.com/buy-used-honda-cars-delhi-ncr/'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        name      = table.find('h3', {'class': '_1Nvyc _1Corb'}).text
        model_date = table.find('li', {'itemprop': 'modelDate'}).text
        model_date = int(model_date)
        engine_1 = table.find('li', {'itemprop': 'vehicleEngine'}).text
        engine = (re.split('•', engine_1))
        engine = ''.join(engine)

        price_1 = table.find('div', {'class': 'col-5 col-md-12 col-xl-5'}).text
        price_2 = (re.split('₹|,|', price_1))
        price = ''.join(price_2)
        price = float(price)

        location = table.find('a', {'class': '_1Kids'}).text

        viwe_1 = table.find('a', {'class': '_3dFtM'}).text
        viwe_2 = (re.split('K Views|Views|', viwe_1))
        viwe_3 = ''.join(viwe_2)
        viwe_3 = float(viwe_3)
        viwe = (viwe_3) * 100

        link = 'https://www.cars24.com/' + table.find('a', {'class': 'qD5mC'}).get('href')

        car_1 = requests.get(link)
        car = car_1.text
        car_soup = BeautifulSoup(car, 'html.parser')

        emi_1 = car_soup.find('span', {'class': '_3N4Rp'})
        emi_2 = emi_1.text if emi_1 else "N/A"
        emi_3 = (re.split('EMI starts @|,|', emi_2))
        emi_4 = ''.join(emi_3)
        if emi_4 != "N/A":
            emi = float(emi_4)
        else:
            emi = 'null'

        overviews = car_soup.find('ul', {"class": "_1wIhE"})
        for overview in overviews:
            detail = overview.text
            if detail[0] == 'C':
                car_id = (detail[6:-1] + detail[-1])
            elif detail[0] == 'K':
                km_driven = (detail[10:-1] + detail[-1])
            elif detail[0] == 'F':
                fuel_type = (detail[9:-1] + detail[-1])
            elif detail[0] == 'O':
                owner = (detail[5:-1] + detail[-1])
            elif detail[0] == 'T':
                transmission = (detail[12:-1] + detail[-1])
            elif detail[0] == 'R':
                rot = (detail[3:-1] + detail[-1])

        cars_no = cars_no + 1
        Cars_dict[cars_no] = [name, model_date, engine, location, viwe, price, link, emi, car_id, km_driven, fuel_type, owner,
                              transmission, rot]

        no_page =  no_page + 1
        no_page =  str(no_page)
        url     = 'https://www.cars24.com/buy-used-honda-cars-delhi-ncr/' + '?page=' + no_page
        no_page =  int(no_page)

cars_dict_df = pd.DataFrame.from_dict(Cars_dict, orient='index',
                                      columns=['Name_of_car', 'Model_Date', 'Engine', 'Location', 'Viwe', 'Price_Rs',
                                           'Link', 'Emi_Starts_At :', 'Car_ID', 'KmS_Driven', 'Fuel_Type', 'Owner',
                                           'Transmission', 'RTO'])

cars_dict_df

cars_dict_df.to_csv('about_cars24.csv')
