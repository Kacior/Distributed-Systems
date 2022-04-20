from http.client import INTERNAL_SERVER_ERROR
from flask import Flask, render_template, request, g
import requests
import json
import concurrent.futures as cf
import jinja2
import werkzeug
import werkzeug.exceptions
app = Flask(__name__, template_folder='templates')
app.config["PROPAGATE_EXCEPTIONS"] = False

api_key = '99e70307ec79271ea2ac9f374d752a2c7f9a5bce'

@app.template_filter('parse')
def parse(s):
    s = str(s)
    s = s.replace('{', '')
    s = s.replace('}', '')
    s = s.replace(':', '')
    s = s.replace("'", '')
    s = s[2:]
    return s

jinja2.filters.FILTERS['parse']  = parse

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def internal_server_error_handler(error_code):
    return render_template('error.html')

app.register_error_handler(werkzeug.exceptions.InternalServerError, internal_server_error_handler)


@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == "POST":
        name = request.form["nm"]
        date = request.form["dt"]
        ct1 = request.form["ct1"]
        ct2 = request.form["ct2"]
        ct3 = request.form["ct3"]

        date_details = date.split("-")
        valid_c = True
        valid_n = True
        flag_name = True
        #[0] = year, [1] = month, [2] = day
        if name == '':
            valid_n = False
            flag_name = False
            return render_template('countries.html', valid_name = valid_n)

        if ct1 == 'none' and ct2 == 'none' and ct3 == 'none':
            valid_c = False
            return render_template('countries.html', pre_date = date, pre_name = name, valid_city = valid_c)

        json_data = []

        with cf.ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_holiday, year = date_details[0], month = date_details[1], day = date_details[2], country = ct1),
            executor.submit(get_holiday, year = date_details[0], month = date_details[1], day = date_details[2], country = ct2),
            executor.submit(get_holiday, year = date_details[0], month = date_details[1], day = date_details[2], country = ct3)]
            for future in cf.as_completed(futures):
                json_data.append(future.result())
                print(future.result())
        
        not_found = False
        if json_data == [[], [], []]:
            not_found = True

        cities = [ct1, ct2, ct3]
        namedays_info = []

        with cf.ThreadPoolExecutor() as executor:
            futures = []
            for city in cities:
                if city != 'none':
                    futures.append(executor.submit(get_nameday, country = city))
            for future in cf.as_completed(futures):
                print(future.result())
                if 'error' in future.result():
                    pass
                else:
                    namedays_info.append(future.result())

        return render_template('countries.html',flag_name = flag_name, not_found = not_found, valid_city = valid_c, name_v = name, data = json_data, namedays = namedays_info)
    return render_template('countries.html', flag_name = False)


def get_holiday(year, month, day, country):
    url = 'https://calendarific.com/api/v2/holidays?&api_key={}&country={}&year={}&month={}&day={}'.format(api_key, country, year, month, day)
    req = requests.get(url)
    data = req.content
    json_data = json.loads(data)
    return json_data['response']['holidays']

def get_nameday(country):
    country = country.lower()
    url = 'https://nameday.abalin.net/api/V1/today?country={}'.format(country)
    req = requests.get(url)
    data = req.content
    json_data = json.loads(data)
    return json_data


if __name__ == "__main__":
    app.run()