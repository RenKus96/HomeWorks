from flask import Flask
from faker import Faker
import csv

app = Flask(__name__)

@app.route("/avr_data")
def get_avr_data():
    with open("hw.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter = ",")
        out_str = '<h3> Список студентов из файла hw.csv:</h3>'
        out_str += '<p>'
        count = 0
        height_sum = 0.0
        weight_sum = 0.0
        for row in file_reader:
            if count > 0:
                height_sum += float(row[1])
                weight_sum += float(row[2])
            count += 1
        # отнимаем от счётчика единицу, что бы получить общее количество студентов (минусуем первую строку с заголовками)
        count -= 1 
        out_str += ' Общее количество студентов - {}<br>'.format(count)
        out_str += ' Средний рост: в дюймах - {:.2f}, в сантиметрах - {:.1f}<br>'.format(height_sum/count, height_sum*2.54/count)
        out_str += ' Средний вес: в фунтах - {:.2f}, в килограммах - {:.2f}'.format(weight_sum/count, weight_sum*0.453592/count)
        out_str += '</p>'
    return out_str

@app.route("/requirements")
def get_requirements():
    f_req = open('requirements.txt')
    out_str = '<h3> Содержимое файла requirements.txt:</h3>'
    out_str += '<p>'
    for cnt,module in enumerate(f_req):
        out_str += '{}. {}<br>'.format(cnt+1,module)
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