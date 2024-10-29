from flask import Flask, render_template, request
import requests
app = Flask(__name__)


api_key = 'db9a03b420d9ac617762fd33e6988948'
url_symbols = f"https://data.fixer.io/api/symbols?access_key={api_key}"
url_base = f"https://data.fixer.io/api/latest?access_key={api_key}"
symbols = requests.get(url_symbols).json()
list_symbols = symbols['symbols']


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here

    to_currency = request.form.get('to')
    amount = request.form.get('amount')
    answer = ''

    if to_currency and amount and request.method == 'POST':
        try:
            amount = float(amount)
            querystring = {"base": 'EUR'}
            response = requests.get(url_base, params=querystring)

            if response.status_code == 200:
                data = response.json()

                if 'rates' in data and to_currency in data['rates']:
                    rate = data['rates'][to_currency]
                    answer = f'{amount} Euros is worth {amount * rate:.2f} {symbols['symbols'][to_currency]}'
                else:
                    answer = 'Currency not available'
            else:
                answer = 'API request failed'
        except ValueError:
            answer = 'Invalid amount format'


    return render_template(
        "home.html",
        symbols=list_symbols,
        answer=answer,
    )


if __name__ == '__main__':
    app.run(debug=True)
