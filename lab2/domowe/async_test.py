from flask import Flask, render_template, request, g
import requests
import json
import asyncio
import time
import concurrent.futures as cf

app = Flask(__name__, template_folder='templates')

api_key = '99e70307ec79271ea2ac9f374d752a2c7f9a5bce'

@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == "POST":
        name = request.form["nm"]
        date = request.form["dt"]
        ct1 = request.form["ct1"]
        ct2 = request.form["ct2"]
        ct3 = request.form["ct3"]

        date_details = date.split("-")
        print(ct1+' '+ct2+' '+ct3)
        #[0] = year, [1] = month, [2] = day
        if ct1 == 'none' and ct2 == 'none' and ct3 == 'none':
            pass

        start = time.time()

        with cf.ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_holiday_s, year = date_details[0], month = date_details[1], day = date_details[2], country = ct1),
            executor.submit(get_holiday_s, year = date_details[0], month = date_details[1], day = date_details[2], country = ct2),
            executor.submit(get_holiday_s, year = date_details[0], month = date_details[1], day = date_details[2], country = ct3)]
            for future in cf.as_completed(futures):
                print(future.result())
        
        end = time.time()

        print(f"future = {end-start}")

        start = time.time()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [get_holiday(date_details[0], date_details[1], date_details[2], ct1),
        get_holiday(date_details[0], date_details[1], date_details[2], ct2),
        get_holiday(date_details[0], date_details[1], date_details[2], ct3)]

        a, b, c = loop.run_until_complete(asyncio.gather(*tasks))
        print(a)
        print(b)
        print(c)
        loop.close()

        end = time.time()
        print(f"async = {end-start}")

        start = time.time()

        a = get_holiday_s(date_details[0], date_details[1], date_details[2], ct1)
        b = get_holiday_s(date_details[0], date_details[1], date_details[2], ct2)
        c = get_holiday_s(date_details[0], date_details[1], date_details[2], ct3)

        end = time.time()
        print(f"sync = {end-start}")

        json_data = []
        json_data.append(a)
        json_data.append(b)
        json_data.append(c)

        #print(json_data)

       # json_data.append(get_holiday(date_details[0], date_details[1], date_details[2], ct1))
        #json_data.append(get_holiday(date_details[0], date_details[1], date_details[2], ct2))
        #json_data.append(get_holiday(date_details[0], date_details[1], date_details[2], ct3))
    return render_template('countries.html', name_v = name, data = json_data)
   
@asyncio.coroutine
def get_holiday(year, month, day, country):
    url = 'https://calendarific.com/api/v2/holidays?&api_key={}&country={}&year={}&month={}&day={}'.format(api_key, country, year, month, day)
    req = requests.get(url)
    data = req.content
    json_data = json.loads(data)
    return json_data['response']['holidays']

def get_holiday_s(year, month, day, country):
    url = 'https://calendarific.com/api/v2/holidays?&api_key={}&country={}&year={}&month={}&day={}'.format(api_key, country, year, month, day)
    req = requests.get(url)
    data = req.content
    json_data = json.loads(data)
    return json_data['response']['holidays']


if __name__ == "__main__":
    app.run()