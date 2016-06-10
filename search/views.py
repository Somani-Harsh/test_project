import requests
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from pandas.io.json import json_normalize
# from pandas.core.frame import DataFrame


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

	print latitude, longitude
	
	return latitude, longitude



def home(request):
	try:
		print request.GET
		location = request.GET.get('location')
	except:
		location = None


	print location 

	if location:
		lat, lon = get_location(location)
		a =get_restaurants(lat,lon)
		custom = []

		count = 0 
		# for item in a['restaurants']:
		# 	count += 1
		# 	print count
		# 	#restaurants and the total number of reviews, and rating, cost e.t.c.

		# 	t = item['restaurant']

			
			
			# custom.append({t['id']:{
			# 		'name':t['name'],
			# 		'rating':t['user_rating'],
			# 		# 'cost':t['average_cost_for_two'],
			# 		# 'review' : reviews
			# 		}})
			# if count==2:
			# 	break		
			
		# a = get_restaurants()

		restaurants = json_normalize( a['restaurants'])
		print restaurants.to_html()
		return HttpResponse(restaurants.to_html())
		# print restaurants

		return render_to_response("result.html",{'a':custom},context_instance=RequestContext(request))
	else:
		return render_to_response("home.html",{},context_instance=RequestContext(request))