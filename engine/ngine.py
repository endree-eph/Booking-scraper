from bs4 import BeautifulSoup


def get_link(hotel):
    try:
        link=hotel.find("a")["href"]
    except:
        link=""
    return link

def get_name(hotel):
    try:
        name=hotel.find("div", class_="fcab3ed991 a23c043802").text.strip()
    except:
        name=""
    return name

def get_img(hotel):
    try:        
        image = hotel.find("img", class_="b8b0793b0e")["src"]
    except:
        image=""
    return image

def get_price(hotel):
    try:
        price = hotel.find("span", class_="fcab3ed991 fbd1d3018c e729ed5ab6").text.strip("€ ")
    except:
        price=""
    return price

def get_score(hotel):
    try:
        score = hotel.find("div", class_="b5cd09854e d10a6220b4").text.strip()
    except:
        score=""
    return score

def get_near(hotel):
    try:
        near =  hotel.find("span", class_="acb0d5ead1").text.strip()
    except:
        near=""
    return near

def get_address(hotel):
    try:
        address = hotel.find("span", class_="f4bd0794db b4273d69aa").text.strip()
    except:
        address = ""
    return address

