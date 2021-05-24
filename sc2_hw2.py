from flask import Flask
from faker import Faker
import csv

INCH_TO_CM = 2.54
POUND_TO_KG = 0.453592

app = Flask(__name__)

@app.route("/avr_data")
def get_avr_data():
    with open("hw.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ",")
        out_str = '<h3> Список студентов из файла hw.csv:</h3>'
        out_str += '<p>'
        count = 0
        height_sum = 0.0
        weight_sum = 0.0
        for row in file_reader:
            count += 1
            # out_str += '{}. {}<br>'.format(count,row)
            height_sum += float(row[' "Height(Inches)"'])
            weight_sum += float(row[' "Weight(Pounds)"'])
        out_str += ' Общее количество студентов - {}<br>'.format(count)
        out_str += ' Средний рост: в дюймах - {:.2f}, в сантиметрах - {:.1f}<br>'.format(height_sum/count, height_sum*INCH_TO_CM/count)
        out_str += ' Средний вес: в фунтах - {:.2f}, в килограммах - {:.2f}'.format(weight_sum/count, weight_sum*POUND_TO_KG/count)
        out_str += '</p>'
    return out_str

@app.route("/requirements")
def get_requirements():
    out_str = '<h3> Содержимое файла requirements.txt:</h3>'
    out_str += '<p>'
    with open('requirements.txt') as f_req:
        for cnt,module in enumerate(f_req, 1):
            out_str += '{}. {}<br>'.format(cnt, module)
        out_str += '</p>'
    return out_str

@app.route("/random_students")
def get_random_students():
    out_str = '<h3> Список десяти наших лучших студентов:</h3>'
    out_str += '<p>'
    fake = Faker()
    for cnt in range(10):
        out_str += '{}. {}<br>'.format(cnt+1,fake.name())
    return out_str

@app.route('/about')
def about():
    return '<p>Это домашнее задание №2<br>по теме: "Знакомство с Flask"</p>'

if __name__ == "__main__":
    app.run(debug=True)