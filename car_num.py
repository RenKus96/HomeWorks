# -*- coding: utf-8 -*-
import re

def Car_num_check(s):
    car_reg = ('^[А-ЯІ]{2}\d{4}[А-ЯІ]{2}$','^\d{2} \d{3}-\d{2}[А-ЯІ]{2}$','^[А-ЯІ]\d{5}[А-ЯІ]{2}$')
    find_nom=False
    for reg_nom in car_reg:
        res = re.findall(reg_nom, s)
        if len(res)==1: find_nom=True
    return find_nom

def yes_no():
    while True:
        s = input('Выберите ДА или НЕТ (Y/N,Д/Н) ')
        if s.lower()=='y':
            res = True
            break
        elif s.lower()=='n':
            res = False
            break
        elif s.lower()=='д':
            res = True
            break
        elif s.lower()=='н':
            res = False
            break
        else:
            print('Надо ответить "Y/N" или "Д/Н".')
    return res

def input_nom():
    while True:
        car_num = input('Введите cтроку c номером машины: ').upper()
        if car_num=='':
            print('Вы не ввели строку c номером машины.')
            continue
        if Car_num_check(car_num):
            print('{} - Это номер машины'.format(car_num))
        else:
            print('{} - Это не номер машины'.format(car_num))
        print('Хотите ввести строку c номером машины ещё раз?')
        if not yes_no():
            print('До встречи.')
            break


if __name__ == '__main__':
    input_nom()        