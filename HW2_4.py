import random
import string
from flask import Flask, request, Response, render_template, Markup
import sqlite3
 
dbname = 'chinook.db'
app = Flask(__name__)

def get_fetch_one(sql):
    try:
        conn = sqlite3.connect(dbname) 
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchone()[0]
            res_ok = True
    except sqlite3.Error as err:
        res = err.args[0]
        res_ok = False
    finally:
        if conn:
            conn.close()
    return res_ok, res

@app.route('/unique_names')
def get_unique_names():
    zag = 'Таблица Customers'
    opis = 'Количество уникальных имен (FirstName) в таблице Customers: '
    sql = "select count(distinct(FirstName)) from Customers"
    res_ok, res = get_fetch_one(sql)
    if res_ok:
        out_str = Markup('<b>{}</b>'.format(res))
    else:
        opis = 'Во время обращения к базе произошла ошибка:'
        out_str = Markup('<br>{}'.format(res))
    return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)
# @app.route('/unique_names')
# def get_unique_names():
#     zag = 'Таблица Customers'
#     opis = 'Количество уникальных имен (FirstName) в таблице Customers: '
#     try:
#         conn = sqlite3.connect(dbname) 
#         with conn:
#             cur = conn.cursor()
#             sql = "select count(distinct(FirstName)) from Customers"
#             cur.execute(sql)
#             out_str = Markup('<b>{}</b>'.format(cur.fetchone()[0]))
#     except sqlite3.Error as err:
#         opis = 'Во время обращения к базе произошла ошибка:'
#         out_str = Markup('<br>'+err.args[0])
#     finally:
#         if conn:
#             conn.close()
#     return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)

@app.route('/tracks_count')
def get_tracks_count():
    zag = 'Таблица Tracks'
    opis = 'Количество записей в таблице Tracks: '
    sql = "select count(*) from Tracks"
    res_ok, res = get_fetch_one(sql)
    if res_ok:
        out_str = Markup('<b>{}</b>'.format(res))
    else:
        opis = 'Во время обращения к базе произошла ошибка:'
        out_str = Markup('<br>{}'.format(res))
    return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)
# @app.route('/tracks_count')
# def get_tracks_count():
#     zag = 'Таблица Tracks'
#     opis = 'Количество записей в таблице Tracks: '
#     try:
#         conn = sqlite3.connect(dbname) 
#         with conn:
#             cur = conn.cursor()
#             sql = "select count(*) from Tracks"
#             cur.execute(sql)
#             out_str = Markup('<b>{}</b>'.format(cur.fetchone()[0]))
#     except sqlite3.Error as err:
#         opis = 'Во время обращения к базе произошла ошибка:'
#         out_str = Markup('<br>'+err.args[0])
#     finally:
#         if conn:
#             conn.close()
#     return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)

@app.route('/sales')
def get_sales():
    zag = 'Таблица Invoice_Items'
    opis = 'Сумма всех продаж компании из таблицы Invoice_Items: '
    sql = "select sum(UnitPrice * Quantity) from Invoice_Items"
    res_ok, res = get_fetch_one(sql)
    if res_ok:
        out_str = Markup('<b>{:.2f}</b>'.format(res))
    else:
        opis = 'Во время обращения к базе произошла ошибка:'
        out_str = Markup('<br>{}'.format(res))
    return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)
# @app.route('/sales')
# def get_sales():
#     zag = 'Таблица Invoice_Items'
#     opis = 'Сумма всех продаж компании из таблицы Invoice_Items: '
#     try:
#         conn = sqlite3.connect(dbname) 
#         with conn:
#             cur = conn.cursor()
#             sql = "select sum(UnitPrice * Quantity) from Invoice_Items"
#             cur.execute(sql)
#             out_str = Markup('<b>{:.2f}</b>'.format(cur.fetchone()[0]))
#     except sqlite3.Error as err:
#         opis = 'Во время обращения к базе произошла ошибка:'
#         out_str = Markup('<br>'+err.args[0])
#     finally:
#         if conn:
#             conn.close()
#     return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)

@app.route('/customers')
def get_customers():
    city = request.args.get('city')
    country = request.args.get('country')
    sql = 'select * from Customers '
    if city or country:
        sql += 'where '
    if city :
        sql += "City='{}' ".format(city)
    if city and country:
        sql += 'and '
    if country:
        sql += "Country='{}' ".format(country)
    zag = 'Таблица Customers'
    opis = 'Содержимое таблицы Customers с фильтрацией по городу и стране: '
    try:
        conn = sqlite3.connect(dbname) 
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            out_str = ''
            for cnt, row in enumerate(cur.fetchall(), 1):
                out_str += '<br> {}. {}'.format(cnt, row)
            out_str = Markup(out_str)
    except sqlite3.Error as err:
        opis = 'Во время обращения к базе произошла ошибка:'
        out_str = Markup('<br>'+err.args[0])
    finally:
        if conn:
            conn.close()
    return render_template('for_any_data.html', zagolovok = zag, opisanie = opis, data = out_str)


if __name__ == "__main__":
    app.run(debug=True)
