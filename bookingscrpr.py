import sys
import argparse
import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


nombres=[]
links=[]
imagenes=[]
precio=[]
puntuacion=[]
cerca = []
ubicacion = []
is_verbose = True

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(1)

def process_data(people, country, city, datein, dateout, is_detail, limit):
    session = requests.Session()
    #people=2
    #country=""
    #city="Mallorca"
    #datein= datetime.datetime.now()
    #dateout= datetime.datetime.now() + datetime.timedelta(7)
    offset=0

    REQUEST_HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
    BOOKING_PREFIX = 'https://www.booking.com'
    ROW_PER_OFFSET = 25

    starting_url = create_url(people, country, city, datein, dateout, offset)
        # print(starting_url)
    print("[~] Url created:" + "\n" + "\t" + starting_url)
    response = session.get(starting_url, headers=REQUEST_HEADER)

    #with open("response.html") as fp:
    soup = BeautifulSoup(response.text, "html.parser")
    #print(response.text)
        
    hotels=soup.find_all("div", class_="a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942" )


    for hotel in hotels:
        try:
            link=hotel.find("a")["href"]
        except:
            link=""
        try:
            name=hotel.find("div", class_="fcab3ed991 a23c043802").text.strip()
        except:
            name=""
        try:        
            image = hotel.find("img", class_="b8b0793b0e")["src"]
        except:
            image=""
        try:
            price = hotel.find("span", class_="fcab3ed991 bd73d13072").text.strip("€")
        except:
            price=""
        try:
            score = hotel.find("div", class_="b5cd09854e d10a6220b4").text.strip()
        except:
            score=""
        try:
            near =  hotel.find("span", class_="acb0d5ead1").text.strip()
        except:
            near=""
        try:
            address = hotel.find("span", class_="f4bd0794db b4273d69aa").text.strip()
        except:
            address = ""


        nombres.append(name)
        links.append(link)
        imagenes.append(image)
        precio.append(price)
        puntuacion.append(score)
        cerca.append(near)
        ubicacion.append(address)   

    data = {'Nombre': nombres,
        'Link': links,
        'Imagen': imagenes,
        'Precio': precio,  
        'Puntuacion': puntuacion,
        'Cerca' : cerca,
        'Ubicacion' : ubicacion
           
           }   
    df=pd.DataFrame(data)
    return df.to_json(orient="records")

def create_url(people, country, city, datein, dateout, offset):
    url = "https://www.booking.com/searchresults.html?checkin_month={in_month}" \
        "&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}" \
        "&checkout_monthday={out_day}&checkout_year={out_year}&group_adults={people}" \
        "&group_children=0&order=price&ss={city}%2C%20{country}&offset={offset}"\
        .format(in_month=str(datein.month),
                in_day=str(datein.day),
                in_year=str(datein.year),
                out_month=str(dateout.month),
                out_day=str(dateout.day),
                out_year=str(dateout.year),
                people=people,
                city=city,
                country=country,
                offset=offset)
    return url



def retrieve_data(people, country, city, datein, dateout, outdir, is_detail, limit):

    result = []
    if isinstance(datein, str) or isinstance(dateout, str):
        datein = datetime.datetime.strptime(datein, "%Y-%m-%d")
        dateout = datetime.datetime.strptime(dateout, "%Y-%m-%d")

    result = process_data(people, country, city, datein, dateout, is_detail, limit)

    if outdir == "":
        outdir = ("./" + country + city + "_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".json").replace(" ", "_").replace(":", "_")

    if is_verbose:
        print("[~] Saving under the path: " + outdir)

    with open(outdir, 'w', encoding='utf-8') as f:
        parse = json.loads(result)
        json.dump(parse, f, ensure_ascii=False, indent=4)
        #f.writelines(result)
        f.close()
    #print(result)
    print("[~] Process finished!")



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--people",
                        help='Used to specify the number of people to the booking request.',
                        default=1,
                        type=int)
    parser.add_argument("--country",
                        help='Used to specify the country to the booking request.',
                        default='')
    parser.add_argument("--city",
                        help='Used to specify the city to the booking request.',
                        default='')
    parser.add_argument("--datein",
                        help='Used to specifiy checkin day.',
                        default=today)
    parser.add_argument("--dateout",
                        help='Used to specifiy checkout day.',
                        default=tomorrow)
    parser.add_argument("-o", "--outdir",
                        help='Used to specify the output dir and filename',
                        default="")
    parser.add_argument("-d", '--detail',
                        default=False,
                        help='Use it if you want more details in the output',
                        action='store_true')
    parser.add_argument("-v", '--verbose',
                        default=False,
                        help='Use it if you want more logs during the process',
                        action='store_true')
    parser.add_argument("-l", '--limit',
                        default=-1,
                        type=int,
                        help='Used to specify the number of page to fetch')

    args = parser.parse_args()
    if args.country == '' and args.city == '':
        parser.error('No action performed, use the --city or --country param at least')
    if args.verbose:
        is_verbose = True

    retrieve_data(args.people, args.country, args.city, args.datein, args.dateout, args.outdir, args.detail, args.limit)