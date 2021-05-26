import random
import string
from flask import Flask, request, Response, render_template, Markup
import html
import requests

yes_no = [1,0]
str_len = '100'
app = Flask(__name__)

def check_yes_no(param):
    res = request.args.get(param, '0')
    msg = 'Всё ОК!'
    status = 200
    if res.isdigit():
        res = int(res)
        if res not in yes_no:
            msg = 'Error: Параметр specials должен быть  1 или 0'
            status = 400
    else:
        msg = 'Error: Параметр specials должен быть числовым'
        status = 400
    return res, msg, status

def encode_str_to_html(s):
    return ''.join('&#{:07d};'.format(ord(c)) for c in s)

@app.route('/random')
def get_random():
    length = request.args.get('length', str_len)
    if length.isdigit():
        length = int(length)
        if not (1 <= length <= int(str_len)):
            return Response('Error: Параметр length должен быть в приделах от 1 до {}'.format(str_len), status=400)
    else:
        return Response('Error: Параметр length должен быть числовым',status=400)

    # specials = request.args.get('specials', '0')
    # if specials.isdigit():
    #     specials = int(specials)
    #     if specials not in yes_no:
    #         return Response('Error: Параметр specials должен быть  1 или 0', status=400)
    # else:
    #     return Response('Error: Параметр specials должен быть числовым',status=400)
    specials, msg, status = check_yes_no('specials')
    if status != 200:
        return Response(msg, status = status)

    # digits = request.args.get('digits', '0')
    # if digits.isdigit():
    #     digits = int(digits)
    #     if digits not in yes_no:
    #         return Response('Error: Параметр digits должен быть  1 или 0', status=400)
    # else:
    #     return Response('Error: Параметр digits должен быть числовым', status=400)
    digits, msg, status = check_yes_no('digits')
    if status != 200:
        return Response(msg, status = status)

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

def getFromHTTP(fromHTTP):
    try:
        p = requests.get(fromHTTP)
    except requests.exceptions.RequestException as err:
        msg = "Нет доступа к данным {} по причине --> {}\n".format(fromHTTP, err)
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
def get_bitcoin_rate():
    valute = request.args.get('currency', 'USD').upper()
    if not valute.isalpha() or len(valute)!=3:
        return Response('Error: Неверный формат валюты - {}'.format(valute), status=400)
    resOk, rate, msg = getFromHTTP("https://bitpay.com/api/rates/{}".format(valute))
    if resOk:
        return render_template('bitcoin_rate.html', name=rate['name'], code=rate['code'], rate=rate['rate'])
    else:
        return Markup.escape(msg)

if __name__ == "__main__":
    app.run(debug=True)
