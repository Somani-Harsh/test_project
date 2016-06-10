import requests
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from pandas.io.json import json_normalize
# from pandas.core.frame import DataFrame
from utils import get_reviews_details, haversine

# Create your views here.


def get_restaurants(latitude="28.6276", longitude="77.2784", establishment_type=1):
	 

	url = 'https://developers.zomato.com/api/v2.1/search'



	# Parameters are basically data sent with the URL
	params = {
			'lat': latitude,
			'lon': longitude,
			'sort': 'rating',
			'order': 'desc',
			'cuisines': 'cuisine',
			'establishment_type': establishment_type,
			# 'entity':"city",
			'radius': 2000.0,
			'count': 100
	}

	header = {
		'User-Agent': 'curl/7.30.0',
		'Accept': 'application/json',
		'user_key': 'a560615348198de6373564df0e3bd857',
	}
	

   
	r = requests.get(
		url=url, headers=header, params=params)


	restaurants = r.json()
	
	

	# This puts the best_rated_restaurants in a list. Refer to JSON Response.
	# restaurants_list = {'restaurants': restaurants['restaurants']}

	return restaurants



def get_location(location):


	api_key = "AIzaSyAP-URITVI1c0RfktFoHX78imOimvcwBps"
	api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(location, api_key))
	api_response_dict = api_response.json()


	if api_response_dict['status'] == 'OK':
		latitude = api_response_dict['results'][0]['geometry']['location']['lat']
		longitude = api_response_dict['results'][0]['geometry']['location']['lng']

	
	return latitude, longitude



def home(request):
	try:
		location = request.GET.get('location')
	except:
		location = None

	if location:
		lat, lon = get_location(location)
		a =get_restaurants(lat,lon)
		custom = []

		count = 0

		for restaurant in a['restaurants']:
			restaurant['restaurant']['review'] = get_reviews_details(restaurant['restaurant']['url'].split("?")[0])
			rlat = float(restaurant['restaurant']['location']['latitude'])
			rlong = float(restaurant['restaurant']['location']['longitude'])

			
			restaurant['restaurant']['distance'] = str(haversine(lon, lat, rlong, rlat))+' km'





		restaurants = json_normalize( a['restaurants'])
		# print restaurants
		return HttpResponse(restaurants.to_html())
		# print restaurants

		# return render_to_response("result.html",{'a':custom},context_instance=RequestContext(request))
	else:
		return render_to_response("home.html",{},context_instance=RequestContext(request))
