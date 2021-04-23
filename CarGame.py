from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import random as rn
import ctypes
import math
import re

# Запускаем браузер
driver = webdriver.Chrome('{your chromedriver path}')
# driver.maximize_window()  # Если нужно запускать в полный экран

# Для цветной консоли
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


# Все цвета для консоли
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


# Все марки
data = [["ac",
         "amc",
         "acura",
         "adler",
         "alfa romeo",
         "alpina",
         "ariel",
         "aro",
         "asia",
         "aston_martin",
         "audi",
         "austin",
         "bmw",
         "byd",
         "bajaj",
         "bentley",
         "borgward",
         "brilliance",
         "buick",
         "cadillac",
         "chana",
         "changfeng",
         "changan",
         "changhe",
         "chery",
         "chevrolet",
         "chrysler",
         "citroen",
         "dkw",
         "ds",
         "dw hower",
         "dacia",
         "dadi"], ["daewoo",
                   "daihatsu",
                   "daimler",
                   "datsun",
                   "deco_rides",
                   "delage",
                   "derways",
                   "dodge",
                   "dongfeng",
                   "doninvest",
                   "eagle",
                   "excalibur",
                   "faw",
                   "fso",
                   "ferrari",
                   "fiat",
                   "fisker",
                   "ford",
                   "foton",
                   "gac",
                   "gmc",
                   "geely",
                   "genesis",
                   "geo",
                   "great_wall",
                   "hafei",
                   "haima",
                   "hanomag",
                   "haval",
                   "hawtai",
                   "heinkel",
                   "honda",
                   "huanghai"], ["hummer",
                                 "hyundai",
                                 "infiniti",
                                 "innocenti",
                                 "iran_khodro",
                                 "isuzu",
                                 "jac",
                                 "jmc",
                                 "jaguar",
                                 "jeep",
                                 "jinbei",
                                 "kia",
                                 "vaz",
                                 "lamborghini",
                                 "lancia",
                                 "land_rover",
                                 "landwind",
                                 "lexus",
                                 "liebao",
                                 "lifan",
                                 "lincoln",
                                 "lotus",
                                 "luxgen",
                                 "mg",
                                 "mini",
                                 "mahindra",
                                 "marussia",
                                 "maruti",
                                 "maserati",
                                 "maybach",
                                 "mazda",
                                 "mclaren",
                                 "mercedes"], ["mercury",
                                               "metrocab",
                                               "mitsubishi",
                                               "mitsuoka",
                                               "nissan",
                                               "oldsmobile",
                                               "opel",
                                               "puch",
                                               "packard",
                                               "peugeot",
                                               "plymouth",
                                               "pontiac",
                                               "porsche",
                                               "proton",
                                               "rambler",
                                               "ravon",
                                               "renault",
                                               "samsung",
                                               "rolls_royce",
                                               "rover",
                                               "seat",
                                               "saab",
                                               "santana",
                                               "saturn",
                                               "scion",
                                               "shanghai_maple",
                                               "shuanghuan",
                                               "skoda",
                                               "smart",
                                               "ssangyong",
                                               "subaru",
                                               "suzuki"], ["tata",
                                                           "tatra",
                                                           "tesla",
                                                           "tianma",
                                                           "tianye",
                                                           "tofas",
                                                           "toyota",
                                                           "trabant",
                                                           "triumph",
                                                           "vauxhall",
                                                           "volkswagen",
                                                           "volvo",
                                                           "vortex",
                                                           "wanderer",
                                                           "wartburg",
                                                           "wiesmann",
                                                           "willys",
                                                           "xinkai",
                                                           "zx",
                                                           "zotye",
                                                           "avtokam",
                                                           "gaz",
                                                           "promo_auto",
                                                           "zaz",
                                                           "zil",
                                                           "zis",
                                                           "ig",
                                                           "luaz",
                                                           "moscvich",
                                                           "smz",
                                                           "tagaz",
                                                           "uaz"]]

# Игра на троих
countOfPlayers = 3
roundsCount = 1
priceArray = []

try:
    while (True):

        # Чтобы убрать начальный город из поиска
        if (roundsCount == 1):
            driver.get("https://auto.ru/ryazan/")
            input("Выбери нужный радиус поиска и нажми Enter\n")

        numberOfActivePlayer = 1  # Номер игрока

        # Разделение раундов
        print(color.blue + "======================================" + str(
            roundsCount) + "======================================" + color.end)

        # Цикл через всех игроков
        while (numberOfActivePlayer != countOfPlayers + 1):
            print(color.cyan + "Машина игрока " + str(numberOfActivePlayer) + ":" + color.end)

            def ResultOfRound():
                global countOfPlayers, priceArray

                winner = priceArray.index(max(priceArray)) + 1
                loser = priceArray.index(min(priceArray)) + 1

                print(color.purple + "------------------------")
                print("Победил игрок: " + color.green + str(winner) + color.end)
                print(color.purple + "На последнем месте: " + color.yellow + str(loser) + color.end)
                print(color.purple + "------------------------")
                priceArray.clear()


            # Считает какая машина по счёту, относительно верха и низа
            def PrintNumberOfCar(random_car, CurrentPage):
                global numberOfActivePlayer, countOfPlayers, priceArray

                cars = driver.find_elements_by_class_name('Link.ListingItemTitle-module__link')
                x = 1

                for car in cars:
                    if(x == random_car):
                        driver.get(car.get_attribute('href'))
                        print("Открыта ссылка с машиной")
                        
                        price = re.sub(r'\D', '', WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'OfferPriceCaption__price'))).text)
                        
                        priceArray.append(int(price))
                        if(numberOfActivePlayer == countOfPlayers):
                            ResultOfRound()
                            priceArray.clear()
                        # print("Не удалось открыть вкладку, машина марки " + data[Stolb][Stroka] + " страница: " + str(CurrentPage) + " номер: 1")
                    x += 1


            def ChoosingPage(pages_ready, quantity):
                # Если только одна страница, то выводим её и выбираем случайную машину
                if (pages_ready == 1):
                    # print('\n' + 'Страница номер ' + color.green + '1' + color.end)   # Если нужно выводить номер страницы
                    random_car = rn.randint(1, int(quantity))
                    PrintNumberOfCar(random_car, 1)
                else:
                    # Выбираем случайную страницу
                    Current_page = rn.randint(1, pages_ready)
                    # print('\n' + 'Страница номер: ' + color.green + str(Current_page) + color.end)    # Если нужно выводить номер страницы

                    # Открываем нужную страницу, в зависимости от её номера меняется ссылка
                    if (Current_page < 10):
                        driver.get('https://auto.ru/cars/' + data[Stolb - 1][Stroka - 1] + '/all/?page=' + str(Current_page) + '&output_type=list')
                    else:
                        driver.get('https://auto.ru/cars/' + data[Stolb - 1][Stroka - 1] + '/all?output_type=list&page=' + str(Current_page))

                    # Если последняя страница, то считаем сколько на ней машин
                    if (Current_page == pages_ready):
                        random_car = rn.randint(1, int(quantity) - (int(pages_ready) - 1) * 37)
                        PrintNumberOfCar(random_car, Current_page)
                    else:
                        random_car = rn.randint(1, 37)
                        PrintNumberOfCar(random_car, Current_page)


            #   Округляем кол-во страниц
            def int_r(pages_raw):
                pages_ready = int(pages_raw + (0.5 if pages_raw > 0 else -0.5))
                return pages_ready


            def Pages(quantity):
                #   Считаем сколько всего страниц, чтобы потом округлить
                pages_raw = float(quantity) / 37

                if (int(quantity) >= 3663):  # Если марок больше, чем 3663, то всего 99 страниц
                    pages_ready = 99
                elif (int(quantity) <= 37):  # Если марок меньше, чем 37, то всего 1 страница
                    pages_ready = 1
                else:
                    pages_ready = int_r(pages_raw)  # Иначе округляем кол-во страниц
                return ChoosingPage(pages_ready, quantity)


            def TryFindQuantity():
                # Пытаемся найти кол-во машин выбранной марки на сайте
                try:
                    quantity = re.sub(r'\D', '', WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ButtonWithLoader__content'))).text)
                    Pages(quantity)
                    # print("Число машин: " + color.green + quantity + color.end) # Если нужно выводить число машин
                except:
                    print(color.red + "Error, can't find count of cars, rerun" + color.end)
                    RandBrand()


            def RandBrand():
                global Stolb, Stroka
                # Выбираем марку
                start_number = rn.randint(1, 124)
                # print('Марка номер: ' + color.green + str(start_number) + '\n' + color.end)  # Если нужно вывести номер марки

                # Считаем в какой строке находится эта марка
                Stroka = math.ceil(start_number / 5)
                # print('Строка номер: ' + color.green + str(Stroka) + color.end)  # Если нужно вывести номер строки

                # Если номер марки меньше 5, значит, в первой столбе
                if (start_number <= 5):
                    Stolb = 1
                else:  # Если номер марки больше 5 считаем в какой она столбе
                    Stolb = start_number - (Stroka - 1) * 5
                # print('Столб номер: ' + color.green + str(Stolb) + color.end)  # Если нужно вывести номер столба

                # Открываем ссылку с выбранной маркой
                driver.get('https://auto.ru/cars/' + data[Stolb - 1][Stroka - 1] + '/all/')
                TryFindQuantity()

            RandBrand()

            # Машина следующего игрока
            print(color.yellow + '-------------------------------------------------------------------' + color.end)

            # Если выбирается машина не для последнего игрока, то открываем новую вкладку
            if (numberOfActivePlayer < countOfPlayers):
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])

            numberOfActivePlayer += 1  # Ход следующего игрока

        roundsCount += 1  # Увеличиваем счётчик раундов
        input("Нажмите, чтобы начать след. раунд")
finally:
    driver.quit()
