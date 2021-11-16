from re import findall
from bs4 import BeautifulSoup
import requests
import urllib.request
from requests.api import head

def hotelinfoscraper(hotelname):
    baseurl = "https://www.booking.com"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url = 'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaKsBiAEBmAExuAEXyAEV2AEB6AEB-AECiAIBqAIDuALlm-iCBsACAdICJDA2ZmQ1ZDNjLTQ4MmMtNGU4NC1hZjAwLWY1YTM5ODZlMzdjZNgCBeACAQ&sid=fb49eb8d798a04bade627beb7783ec27&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaKsBiAEBmAExuAEXyAEV2AEB6AEB-AECiAIBqAIDuALlm-iCBsACAdICJDA2ZmQ1ZDNjLTQ4MmMtNGU4NC1hZjAwLWY1YTM5ODZlMzdjZNgCBeACAQ%3Bsid%3Dfb49eb8d798a04bade627beb7783ec27%3Bsb_price_type%3Dtotal%26%3B&ss='+hotelname+'&is_ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=mem&dest_id=&dest_type=&search_pageview_id=5f626f327a62002d&search_selected=false'

    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    toppickhotel =soup.find('a',class_='js-sr-hotel-link hotel_name_link url')
    # print(toppickhotel['href'])
    # print(type(toppickhotel['href']))
    toppickhotellink = toppickhotel['href']
    toppickhotellink = toppickhotellink[2:]
    hotelname = soup.find('span',class_='sr-hotel__name')
    hotelnamefinal = hotelname.text
    urlforhotel = baseurl +'/'+toppickhotellink
    # print(urlforhotel)
    r.close()
    # hotelinfo=soup.find('div',class'hotel_desc')


    r1 = requests.get(urlforhotel,headers=headers)

    soup1 = BeautifulSoup(r1.content, 'lxml')
    # print(soup1)
    hotelinfodiv =soup1.find('div',id='property_description_content')
    # print(hotelinfodiv)
    paragraph = hotelinfodiv.find('p')
    # print(paragraph.text)
    hotelinfofinal = paragraph.text


    atag = soup1.find('div',class_='gallery-side-reviews-wrapper')
    imagelink =atag.find('a',class_='bh-photo-grid-item bh-photo-grid-photo1 active-image')
    imagelinkfinal =imagelink['href']

    return hotelinfofinal,imagelinkfinal,hotelnamefinal,urlforhotel


# info, image = hotelinfoscraper('hyatt')
# print(info)
# print(image)




