import os
from flask import Flask, request, Response, render_template, Markup
from webargs.flaskparser import use_kwargs
from webargs import fields, validate, ValidationError
import sqlite3
 
db_name = os.path.join(os.getcwd(), 'chinook.db')
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

def check_name(param):
    if not param.isalpha():
        raise ValidationError('Invalid name format - {}'.format(param))

def get_fetch_one(sql):
    conn = sqlite3.connect(db_name) 
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchone()[0]
    return res

def get_fetch_all(sql):
    conn = sqlite3.connect(db_name) 
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        fields = [desc[0] for desc in cur.description]
    return res, fields

@app.route('/unique_names')
def get_unique_names():
    header = 'Таблица Customers'
    description = 'Количество уникальных имен (FirstName) в таблице Customers: '
    sql = "select count(distinct(FirstName)) from Customers"
    res = get_fetch_one(sql)
    out_str = Markup('<b>{}</b>'.format(res))
    return render_template('for_any_data.html', header = header, description = description, data = out_str)

@app.route('/tracks_count')
def get_tracks_count():
    header = 'Таблица Tracks'
    description = 'Количество записей в таблице Tracks: '
    sql = "select count(*) from Tracks"
    res = get_fetch_one(sql)
    out_str = Markup('<b>{}</b>'.format(res))
    return render_template('for_any_data.html', header = header, description = description, data = out_str)

@app.route('/sales')
def get_sales():
    header = 'Таблица Invoice_Items'
    description = 'Сумма всех продаж компании из таблицы Invoice_Items: '
    sql = "select sum(UnitPrice * Quantity) from Invoice_Items"
    res = get_fetch_one(sql)
    out_str = Markup('<b>{:.2f}</b>'.format(res))
    return render_template('for_any_data.html', header = header, description = description, data = out_str)

@app.route('/customers')
@use_kwargs({
    "city": fields.Str(
        required=False,
        validate=check_name
    ),
    "country": fields.Str(
        required=False,
        validate=check_name
    )},
    location="query"
)
def get_customers(city=None, country=None):
    sql = 'select * from Customers'
    where_filter = {}
    if city:
        where_filter['City'] = city
    if country:
        where_filter['Country'] = country
    if where_filter:
        sql += ' where ' + ' and '.join('{}=\'{}\''.format(name, value) for name, value in where_filter.items())

    header = 'Таблица Customers'
    description = 'Содержимое таблицы <b>Customers</b> с фильтрацией по <b>городу</b> и <b>стране</b>:<br>'
    res, fields = get_fetch_all(sql)
    out_str = ''
    for cnt, row in enumerate(res, 1):
        out_str += '<br> <b>{}</b>.  {}'.format(cnt, ', '.join('<b>{}</b>=\'{}\''.format(fld,str(s)) for fld,s in zip(fields,row)))
    return render_template('for_any_data.html', header = header, description = Markup(description), data = Markup(out_str))

if __name__ == "__main__":
    app.run(debug=True)
