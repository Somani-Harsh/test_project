import re
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize

def get_reviews_details(url):
    with requests.Session() as session:
        session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
        r = session.get(url + "/reviews")
        soup = BeautifulSoup(r.content, "html.parser")
        itemid = soup.body["itemid"]

        # get reviews
        r = session.post("https://www.zomato.com/php/social_load_more.php", data={
            "entity_id": itemid,
            "profile_action": "reviews-top",
            "page": "0",
            "limit": "1000"
        })
        reviews = r.json()["html"]

        soup = BeautifulSoup(reviews, "html.parser")

        like_data = soup.select("div.js-activity-like-count")
        comment = {}
        count = 0
        for item in like_data:
            count += 1
            like = int(re.search(r'\d+', item.get_text()).group())
            comment.update({count:{'like':like}})

        """rating_data = soup.select("div.tooltip")
        for item in rating_data:
            print re.findall("\d+\.\d+",str(item["aria-label"]))[0]"""
                                
        
        k_data = soup.select("div.rev-text")
        count = 0
        for item in k_data:
            count += 1
            d = item.get_text()
            a = item.children
            a.next()
            b = a.next()
            c = re.findall("\d+\.\d+",str(b["aria-label"]))[0]
            comment[count].update({"rating":c})

    di = {}
    for a in comment.values():
        if di.has_key(a['rating']):
            di[a['rating']]+= a['like']
        else:
            di[a['rating']] = a['like']
    
    return di
    # comment = json_normalize(comment)

    # return HttpResponse(comment.to_html())
    
        

        

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
