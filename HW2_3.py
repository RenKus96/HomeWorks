import random
import string
from flask import Flask, request, Response, render_template, Markup
from marshmallow.validate import Length
from webargs.flaskparser import use_kwargs
from webargs import fields, validate, ValidationError
# import html
import requests

str_len = 100
app = Flask(__name__)

from flask import jsonify
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

def check_currency(param):
    if not param.isalpha() or len(param)!=3:
        raise ValidationError('Invalid currency format - {}'.format(param))

def encode_str_to_html(s):
    return ''.join('&#{:07d};'.format(ord(c)) for c in s)

@app.route('/random')
@use_kwargs({
    "length": fields.Int(
            required=False,
            missing=str_len,
            validate=[validate.Range(min=1, max=str_len)]
        ),
    "digits": fields.Int(
        required=False,
        missing=0,
        validate=validate.OneOf([0, 1])
    ),
    "specials": fields.Int(
        required=False,
        missing=0,
        validate=validate.OneOf([0, 1])
    )},
    location="query"
)
def get_random(length, digits, specials):

    gen_str = string.ascii_letters
    if specials:
        gen_str += string.punctuation
    if digits:
        gen_str += string.digits

    rand_string = ''.join(random.choice(gen_str) for i in range(length))
    # res_str = '<p><b> Без экранирования:</b></p>'
    # res_str += '<p> Случайная строка - {}</p>'.format(rand_string)
    # res_str += '<p><b> С помощью html.escape():</b></p>'
    # res_str += '<p> Случайная строка - {}</p>'.format(html.escape(rand_string))
    # res_str += '<p><b> С помощью ord():</b></p>'
    # res_str += '<p> Случайная строка - {}</p>'.format(encode_str_to_html(rand_string))
    # return res_str
    return render_template('random_str.html', stroka1=rand_string, stroka2=Markup(rand_string), stroka3=Markup.escape(rand_string))
    # Получается, что через шаблоны экранирование идёт автоматически в отличии вывода через String

def get_from_http(from_http):
    try:
        p = requests.get(from_http)
    except requests.exceptions.RequestException as err:
        msg = "Нет доступа к данным {} по причине --> {}\n".format(from_http, err)
        return False, None, msg
    if p.status_code == 200:
        return True, p.json(), 'Всё ОК!'
    else:
        if p.status_code == 404:
            msg = "Страница с данными не найдена. Возможно вы не верно указали валюту.\n"
            return False, None, msg
        else:
            msg = "Нет доступа к данным --> код ответа {}\n".format(p.status_code)
            return False, None, msg

@app.route('/bitcoin_rate')
@use_kwargs({
    "currency": fields.Str(
        required=False,
        missing='USD',
        # validate=[validate.Length(equal=3)]
        # validate=[validate.Regexp(r'^[A-Za-z]{3}$')],
        validate=check_currency
    )},
    location="query"
)
def get_bitcoin_rate(currency):
    valute = currency.upper()
    resOk, rate, msg = get_from_http("https://bitpay.com/api/rates/{}".format(valute))
    if resOk:
        return render_template('bitcoin_rate.html', name=rate['name'], code=rate['code'], rate=rate['rate'])
    else:
        return Markup.escape(msg)

if __name__ == "__main__":
    app.run(debug=True)
