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

@app.route('/genres_durations')
def get_genre_durations():
    header = 'Таблица Tracks, Genres'
    description = 'Общая длительность треков в таблице в секундах, сгруппированная по музыкальным жанрам:<br> '
    sql = """select genres.Name 'Genre', sum(tracks.Milliseconds)/1000 'Duration' from tracks
                JOIN genres on tracks.GenreId=genres.GenreId
                group by tracks.GenreId"""
    res, fields = get_fetch_all(sql)
    out_str = ''
    for cnt, row in enumerate(res, 1):
        out_str += '<br> <b>{}</b>.  {}'.format(cnt, ', '.join('{}=<b>\'{}\'</b>'.format(fld,str(s)) for fld,s in zip(fields,row)))
    return render_template('for_any_data.html', header = header, description = Markup(description), data = Markup(out_str))

@app.route('/greatest_hits')
@use_kwargs({
    "count": fields.Int(
            required=False,
            validate=[validate.Range(min=1)]
        )},
    location="query"
)
def get_greatest_hits(count=None):
    header = 'Топ {} треков'.format(str(count) if count else '')
    description = 'Список <b>{}</b> самых продаваемых треков:<br> '.format(str(count) if count else '')
    sql = """select tracks.Name Track_Name, ROUND(sum(invoice_items.UnitPrice),2) Income,  sum(invoice_items.Quantity) Quantity  
                from invoice_items 
                join tracks on invoice_items.TrackId=tracks.TrackId
                GROUP by invoice_items.TrackId
                ORDER by Income DESC"""
    if count:
        sql += ' LIMIT {}'.format(str(count))
    res, fields = get_fetch_all(sql)
    out_str = ''
    for cnt, row in enumerate(res, 1):
        out_str += '<br> <b>{}</b>.  {}'.format(cnt, ', '.join('{}=<b>\'{}\'</b>'.format(fld,str(s)) for fld,s in zip(fields,row)))
    return render_template('for_any_data.html', header = header, description = Markup(description), data = Markup(out_str))

@app.route('/greatest_artists')
@use_kwargs({
    "count": fields.Int(
            required=False,
            validate=[validate.Range(min=1)]
        )},
    location="query"
)
def get_greatest_artists(count=None):
    header = 'Топ {} исполнителей'.format(str(count) if count else '')
    description = 'Список <b>{}</b> самых продаваемых исполнителей:<br> '.format(str(count) if count else '')
    sql = """select artists.Name Artist_Name, ROUND(sum(invoice_items.UnitPrice),2) Income,  sum(invoice_items.Quantity) Quantity  
                from invoice_items 
                join tracks on invoice_items.TrackId = tracks.TrackId
                join albums on tracks.AlbumId = albums.AlbumId
                join artists on albums.ArtistId = artists.ArtistId
                GROUP by artists.ArtistId
                ORDER by Income DESC"""
    if count:
        sql += ' LIMIT {}'.format(str(count))
    res, fields = get_fetch_all(sql)
    out_str = ''
    for cnt, row in enumerate(res, 1):
        out_str += '<br> <b>{}</b>.  {}'.format(cnt, ', '.join('{}=<b>\'{}\'</b>'.format(fld,str(s)) for fld,s in zip(fields,row)))
    return render_template('for_any_data.html', header = header, description = Markup(description), data = Markup(out_str))

@app.route('/stats_by_city')
@use_kwargs({
    "genre": fields.Str(
        required=False
    ),
    "count": fields.Int(
            required=False,
            validate=[validate.Range(min=1)]
    )},
    location="query"
)
def get_stats_by_city(genre=None, count=None):
    header = 'Топ городов-меломанов'
    description = 'Список топ городов где слушают <b>{}</b>:<br> '.format(genre if genre else 'музыку')
    sql = """select invoices.BillingCity City, sum(invoice_items.Quantity) Quantity  from invoice_items 
                join invoices on invoice_items.InvoiceId=invoices.InvoiceId
                join tracks on invoice_items.TrackId=tracks.TrackId
                join genres on tracks.GenreId=genres.GenreId"""
    if genre:
        sql += ' where genres.Name=\'{}\''.format(genre)
    sql += ' GROUP by invoices.BillingCity ORDER by Quantity DESC'
    if count:
        sql += ' LIMIT {}'.format(str(count))
    res, fields = get_fetch_all(sql)
    out_str = ''
    for cnt, row in enumerate(res, 1):
        out_str += '<br> <b>{}</b>.  {}'.format(cnt, ', '.join('{}=<b>\'{}\'</b>'.format(fld,str(s)) for fld,s in zip(fields,row)))
    return render_template('for_any_data.html', header = header, description = Markup(description), data = Markup(out_str))

if __name__ == "__main__":
    app.run(debug=True)
