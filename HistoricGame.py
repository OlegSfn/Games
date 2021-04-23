import random as r
import string
import ctypes
import re
import time

# Описание значения цветов
'''
Зелёный - Главное из текста
Циановый - Результат
Красный - Ошибка
Жёлтый - Очки
Фиолетовый - Тип игры
'''

# смена цвета консольного текста
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

game_score = 0  # Объявление основных очков
array = []  # Массив для хранения всех годов, чтобы потом его использовать в качестве оператора Dict.get(array[rand])
first_char = None  # Переменная для просмотра файла на наличие рекорда

# Класс со всеми цветами для текста
class color:
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


# Помощь для пользователя
def help():
    while (True):
        print(
            color.green + '\n/----------------------------------------Помощь----------------------------------------\\\n' + color.end) # Вывеска "Помощщь"
        User_request = input(
            'Если хочешь выйти напиши ' + color.green + "Выход" + color.end + '.'
            '\nЕсли хочешь узнать про режимы напиши название этого режима:'
            '\n' + color.green + '"Даты",\n"Даты с правителями",\n"Деятели",\n"Деятели с правителями",\n"Случайный режим"' + color.end + '.\n'
            'Интересно узнать про систему очков напиши ' + color.green + '"Очки"' + color.end + ': ').lower()

        # Обработка запроса и вывод ответа
        if User_request == 'даты':
            print(
                color.purple + 'Тебе даётся дата начала события, тебе нужно написать дату окончания события' + color.end)
        elif User_request == 'даты с правителями':
            print(color.purple + 'Тебе даётся дата начала события, тебе нужно написать дату окончания события и '
                                 'правителя в это время' + color.end)
        elif User_request == 'деятели':
            print(color.purple + 'Тебе даётся название войны, тебе нужно написать деятелей, писать их нужно в '
                                 'алфавитном порядке,\n '
                                 'правители, в чьих именах есть "ё", писать с ней, запятые и пробелы и заглавные буквы необязательны' + color.end)
        elif User_request == 'деятели с правителями':
            print(color.purple + 'Тебе даётся название войны, тебе нужно написать деятелей, писать их нужно в '
                                 'алфавитном порядке,\n '
                                 'правители, в чьих именах есть "ё", писать с ней, запятые и пробелы и заглавные буквы необязательны,'
                                 'и правителя в это время' + color.end)
        elif User_request == 'очки':
            print(color.purple + 'Тебе начисляется по одному очку за режимы без правителей и по 2 очка за режимы с '
                                 'ними.' + color.end)
        elif (User_request == 'случайный режим'):
            print(color.purple + 'Выбирается случайный режим по заданным критериям')
        elif (User_request == 'выход'):
            start()  # повторный запуск старта программы
            break
        else:
            print(color.red + 'Неудалось понять ваш запрос' + color.end)  # Если ни одна из комманд не введена


# Выбор режима игры
def mode_choice():
    print("Хорошо, давай начнём!\n")
    Choice_Dynast = input('Хочешь потяжелее - выбери режим с правителем (0 - без, 1 - с правителем, 2 - выбрать случайно) - ')
    while(True):
        try:
            return int(Choice_Dynast)
        except:
            print(color.red + "Неверный ввод" + color.end + '\n')
            Choice_Dynast = input('Попробуй ещё раз(0 - без, 1 - с правителем, 2 - выбрать случайно) - ')


# Начало программы
def start():
    print("Привет, это моя историческая игра.\n")
    print("В ней тебе нужно будет угадывать дату окончания события по его началу или дату события по его деятелям и их действиям.\n")
    help_input = input('Если тебе нужна помощь по игре напиши ' + color.green + '"Помощь"' + color.end + ', '
                        'если хочешь начать нажми ' + color.green + '"Enter"' + color.end + ': ').lower()
    if (help_input == 'помощь'):
        help()
start()

# Запись значений выбора пользователя
Choice_Dynast = mode_choice()
# Все даты в игре
Dates = {
    1632: '1634',
    1654: '1667',
    1700: '1721',
    1757: '1762',
    1805: '1807',
    1808: '1809',
    1812: '1812',
    1813: '1814',
    1826: '1828',
    1914: '1918',
    1941: '1945'
}
# Запись дат в массив
for key in Dates:
    array.append(key)
# Описание всех событый
Descr = {
    1632: color.bold + 'Смоленская война.' + color.end + '\nРоссия попыталась отвоевать у Польши Смоленск, однако ей это ' + color.green + 'не удалось. ' + color.end + 'Смоленск остался за поляками.',
    1654: color.bold + 'Русско-польская война.' + color.end + '\nВажную роль здесь сыграло восстание запорожских казаков во главе с Богданом Хмельницким Русские поддержали братский народ, который находился под властью польского короля. ' + color.green + 'Русские и запорожцы одержали в итоге победу над поляками.\n' + color.cyan + 'Результат' + color.end + ' - к России отошли Смоленск и все земли потерянные в смутное время. Речь Посполитая потерпела очень серьезное поражение и была очень ослаблена и в последствие восстановиться уже не смогла.',
    1700: color.bold + 'Северная война.' + color.end + '\nБоевые действия шли между Россией и Швецией. ' + color.green + 'Наше государство одержало победу ' + color.end + 'и присоединило себе часть Финляндии, Прибалтику и получило доступ к Балтийскому морю.',
    1757: color.bold + 'Семилетняя война.' + color.end + '\nВ ней принимали участие почти все европейские государства. Для России эта война проходила по большому счету, как война с Пруссией, императором которой был ' + color.green + 'Фридрих II' + color.end + '. Русские заняли Восточную Прусию, временно занимали Берлин и были очень близки к полному разгрому прусской армии, но в 1762 умерла Елизавета, а на престол взошел Петр III, который считал Фридриха II своим кумиром.' + color.cyan + 'Россией и Пруссией подписали мирный договор, все завоевания были возвращены Фридриху.' + color.end,
    1805: color.bold + '3-я и 4-я коалиции.' + color.end + '\nВ этот период наполеоновских войн между Россией и Францией состоялись ' + color.green + '4 крупных сражения. 2 из которых закончились ничьей, а 2 поражением русской армии' + color.end + '.' + color.cyan + 'После поражения России от Франции под Фридландом в 1807 г. был подписан между этими двумя державами Тильзитский мирный договор.' + color.end,
    1808: color.bold + 'Финская война.' + color.end + '\nПротивостояние Российской империи и Швеции,' + color.green + 'в котором последние потерпели сокрушительное поражение. ' + color.cyan + 'Итогом войны стало присоединение Финляндии к России.' + color.end,
    1812: color.bold + 'Отечественная война.' + color.end + '\nВ этом противостоянии ' + color.green + 'сражались Россия Франция' + color.end + '. В рядах последних сражалась почти вся Европа, так как была захвачена французским императором Наполеоном. ' + color.cyan + 'Война окончилась отступлением французов из российских владений.' + color.end,
    1813: color.bold + 'Заграничные походы русской армии.' + color.end + '\nЭти походы проходили в рамках войны с Францией, которая закончилась в 1814 г. ' + color.cyan + 'взятием Парижа русскими и союзными войсками. В итоге Франция потеряла все земли в Европе, которые она захватила. Россия присоединила себе часть Польши вместе с Варшавой.' + color.end,
    1826: color.bold + 'Русско-персидская война.' + color.end + '\nСтарые враги сражались за господство в Закавказье и Прикаспии. ' + color.cyan + 'В очередной раз Российская империя одержала победу в этом противостоянии и в итоге включила в свой состав по Туркманчайскому мирному договору Эриванское и Нахичеванское ханства.' + color.end,
    1914: color.bold + 'Первая мировая война.' + color.green + '\nРоссийская империя вела боевые действия против Германии, Австро-Венгрии и Османской империи. Нашими союзниками были французы и англичане. ' + color.cyan + 'В 1917 г. в России произошли 2 революции. С приходом к власти большевиков в октябре 1917 г. Россия фактически вышла из войны, а в феврале 1918 г. сделала это официально.' + color.end,
    1941: color.bold + 'Великая Отечественная война.' + color.green + '\nВ этом противостоянии сражались СССР и Германия и это проходило в рамках Второй мировой войны. ' + color.cyan + 'Великая Отечественная война закончилась победой советской армии и захватом Берлина. В итоге Германия была раздроблена на ' + color.green + 'ГДР ' + color.end + 'и ' + color.green + 'ФРГ' + color.end + '. Германия потеряла Восточную Прусию, часть которой отошла к СССР (Кенигсберг и его окресности), а часть к Польше. Так же советское государство закрепило за собой Галицию.'
}

# Все правители
Dynast = {
    1632: 'Михаил I Фёдорович Романов',
    1654: 'Алексей I Михайлович Тишайший',
    1700: 'Пётр I Алексеевич Великий',
    1757: 'Елизавета I Петровна',
    1805: 'Александр I Павлович Благословенный',
    1808: 'Александр I Павлович Благословенный,',
    1812: 'Александр I Павлович Благословенный,',
    1813: 'Александр I Павлович Благословенный,',
    1826: 'Николай I Павлович Незабвенный',
    1914: 'Николай II Александрович Страстотерпец',
    1941: 'Иосиф Виссарионович Сталин'
}


# Вывод, подсъёт и запись очков
def score():
    global bestscore, attemp, first_char

    # Вывод правильных ответов в зависимости от режима игры
    if (Choice_Dynast != 1):
        print(color.red + "Ошибка, правильный ответ: " + color.end + Dates.get(
            year) + '\n\n' + "Прочитай факты про это событие: " + Descr.get(year))
    else:
        print(color.red + "Ошибка, правильный ответ: " + color.end + Dates.get(
            year) + '\n' + color.red + 'А правителем был - ' + color.end + Dynast.get(
            year) + '\n\n' + "Прочитай факты про это событие: " + Descr.get(year))

    print("Вам удалось набрать " + str(game_score) + " очков")      # Вывод очков

    # Проверка наличия лучшего результата и запись его в переменную "bestscore"
    try:
        with open('High_score.txt', 'r') as my_file:
            my_file.seek(0)     # Ставим курсор перед первым символом
            first_char = my_file.read(1)    # Читаем первую цифру
            my_file.seek(0)     # Ставим курсор перед первым символом
            # Если файл пуст то рекорд равен 0
            # Если нет, то берём рекорд из файла
            if(not first_char):
                bestscore = 0
            else:
                bestscore = int(re.sub('\D', '', my_file.read()))
    except:
        f = open('High_score.txt', 'w')
        bestscore = 0
        f.close()

    # Вывод очков относительно рекорда
    if (not first_char):    # Если рекорда ещё нет
        print('\n------------------------------------------------------------------------------\n')
    elif (bestscore == game_score):     # Если рекорд равен очкам в нынешной игре
        print("Ваш счёт совпадает с вашим рекордом")
        print('\n------------------------------------------------------------------------------\n')
    elif (bestscore > game_score):      # Если рекорд больше очков в нынешной игре
        print("До нового рекорда не хватило: " + str(bestscore + 1 - game_score) + " очков")
        print('\n------------------------------------------------------------------------------\n')
    else:       # Если рекорд меньше очков в нынешной игре
        print("Вы побили свой прошлый рекорд на " + str(game_score - bestscore) + " очков")
        print('\n------------------------------------------------------------------------------\n')

    # Присваивание лучшего результата
    if (game_score > bestscore):
        bestscore = game_score

        # Запись в файл лучшего результата
        with open('High_score.txt', 'w') as my_file:
            my_file.seek(0)
            token1 = ''.join(r.choice(string.ascii_uppercase + string.ascii_lowercase + string.punctuation) for x in range(r.randint(1, 32)))
            token2 = ''.join(r.choice(string.ascii_uppercase + string.ascii_lowercase + string.punctuation) for x in range(r.randint(1, 32)))
            my_file.write(token1 + str(bestscore) + token2)


# Игра: Даты
def dates_game(Choice_Dynast):
    global game_score, year  # Передача глобальных данных

    if(Choice_Dynast != 0 and Choice_Dynast != 1):
        print(color.purple + "Рандом" + color.end)
        Choice_Dynast = r.randint(0,1)

    # Вывод типа игры в зависимости от с правителями или без
    if (Choice_Dynast == 0):
        print(color.purple + 'Игра: даты\n\n' + color.end)
    elif(Choice_Dynast == 1):
        print(color.purple + 'Игра: даты с правителями\n\n' + color.end)

    # Цикл игры
    while (True):
        # Подбираем случайную дату
        rand = r.randint(0, len(array) - 1)
        year = array[rand]

        # Ввод и сортировка ответа от пользователя о дате
        UserResult_Date = input(str(year) + ' - ')
        UserResult_Date = re.sub('\D', '', UserResult_Date)

        # Проверка игра с правителем или без
        if (Choice_Dynast == 1):        # Игра с правителем
            # Ввод и сортировка ответа от пользователя о правителе
            UserResult_Dynast = input('А правителем был - ')
            UserResult_Dynast = re.sub('[^а-яА-ЯёЁ]', '', UserResult_Dynast)

            # Проверка ответа
            if (UserResult_Date == Dates.get(year) and UserResult_Dynast == re.sub('[^а-яА-ЯёЁ]', '', Dynast.get(year))):
                print(color.green + "Молодец!\n\n" + color.darkcyan + "Вот несколько интересных фактов: " + color.end + Descr.get(year))
                game_score += 2     # Начисление очков

                # Вывод очков каждый раз, когда они кратны 10
                if (game_score % 10 == 0 and game_score != 0):
                    print(color.yellow + "Поздравляем, вы набрали уже: " + str(game_score) + " очков" + color.end)
                print('\n------------------------------------------------------------------------------\n')
            else:       # Если ответ неверный, то запускаем вывод очков и обнуляем нынешные очки
                score()     # Вывод очков
                game_score = 0      # Обнуление очков из-за неверного ответа

        else:       # Игра без правителя
            # Проверка ответа
            if (UserResult_Date == Dates.get(year)):
                print(color.green + "Молодец!\n\n" + color.darkcyan + "Вот несколько интересных фактов: " + color.end + Descr.get(year))
                game_score += 1     # Начисление очков

                # Вывод очков каждый раз, когда они кратны 10
                if (game_score % 10 == 0 and game_score != 0):
                    print(color.yellow + "Поздравляем, вы набрали уже: " + str(game_score) + " очков" + color.end)
                print('\n------------------------------------------------------------------------------\n')
            else:       # Если ответ неверный, то запускаем вывод очков и обнуляем нынешные очки
                score()     # Вывод очков
                game_score = 0      # Обнуление очков из-за неверного ответа


dates_game(Choice_Dynast)