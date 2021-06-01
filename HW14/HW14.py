# -*- coding: utf-8 -*-


def babl(lst):
    print('\n-= Сортировка пузырьком =-')
    is_sorted = False
    while not is_sorted:
        print('Следующий Этап ')
        is_sorted = True
        for i in range(len(lst) - 1):
            print('Итерация № {} : {}-{}'.format(i,lst[i], lst[i + 1]))
            # print(lst[i], lst[i + 1])
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                is_sorted = False
    return lst
    
def s_babl(lst):
    print('\n-= Сортировка пузырьком без повторений =-')
    for j in range(1,len(lst)-1):
        print('Этап № ',j)
        print('Список на данном этапе:',lst)
        is_sorted = True
        for i in range(len(lst) - j):
            print('Итерация № {} : {}-{}'.format(i,lst[i], lst[i + 1]))
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                is_sorted = False
        if is_sorted: return lst
    # return lst

def cocktail(lst): 
    print('\n-= Коктейльная (Шейкерная, двухсторонняя пузырьковая и т.п.) сортировка =-')
    print('-= без повторений =-')
    j = 0
    while True:
        j += 1
        print('Этап № ',j)
        print('Список на данном этапе:',lst)
        # с повторениями
        # for rng in ( range(len(lst)-1), reversed(range(len(lst)-1)) ):
        # без повторений
        for rng in ( range(len(lst)-j), reversed(range(len(lst)-j)) ):
            is_sorted = True
            for i in rng:
                print('Итерация № {} : {}-{}'.format(i,lst[i], lst[i + 1]))
                if lst[i] > lst[i+1]:  
                    lst[i], lst[i+1] =  lst[i+1], lst[i]
                    is_sorted = False
            if is_sorted: return lst


if __name__ == '__main__':
    lst = [7, 9, 3, 4, 0, 6, 1, 8, 2, 5]
    print('\n Отсортированый список : {}'.format(babl(lst)))

    lst = [7, 9, 3, 4, 0, 6, 1, 8, 2, 5]
    print('\n Отсортированый список : {}'.format(s_babl(lst)))

    lst = [7, 9, 3, 4, 0, 6, 1, 8, 2, 5]
    print('\n Отсортированый список : {}'.format(cocktail(lst)))
