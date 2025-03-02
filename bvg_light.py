#import urllib
from urllib.request import urlopen 
import json

from datetime import datetime
import pytz

import board
import neopixel

import time

#get station ID by using https://v6.bvg.transport.rest/locations?poi=false&addresses=false&query=frankfurtor and updating the query term
stationUID = '900120008'
#how far into the future do you want to check for trains (in minutes)?
check_period_duration = '30'

#API endpoint url
url = 'https://v6.bvg.transport.rest/stops/'+ stationUID + '/departures?duration=' + check_period_duration

#variables to account for walking distance
tram_walk_time = 4
u_walk_time = 6

#lists for the lines
u5_eastbound = []
u5_westbound = []
m10_northbound = []
m10_southbound = []
_21_northbound = []
_21_southbound = []

number_of_pixels = 30

#create the pixel object
pixels = neopixel.NeoPixel(board.D18, number_of_pixels, brightness = 0.5)

#set the colors

#U5_COLOR = (7,213,244)
U5_COLOR = (208,9,107)
M10_COLOR = (10,0,255)
#_21_COLOR = (208,9,107)
_21_COLOR = (7,213,244)



# gets all of the time data and puts it into the lists
def grabber():



    #get the json
    try:
	    #open the url
	    response = urlopen(url)
	    #load response as json
	    data_json = json.loads(response.read())
	    #get the departure data from the json
	    departure_data_json = data_json['departures']
    except:
    	#if you can't get the data, just make it a zero so all of the lights are black
    	departure_data_json = {'line': '0', 'name': '0', 'direction': '0'}
    	print('*******error getting data*******')

    #work with the data
    for i in departure_data_json:

        #function to get the departure time modified by walking time to station
        def get_modified_departure_time(arrive, line_type):
            #turn leave_time_string into a datetime object
            #print(f'arrive = {arrive}')
            try:
            	leave_time = datetime.fromisoformat(arrive)
            	#print(f'leave time = {leave_time}')
            	#convert leave time to UTC
            	leave_time_utc = leave_time.astimezone(pytz.utc)
            	# get current time
            	current_time = datetime.now(pytz.utc)
            	# get difference between leave time and current time
            	time_difference = leave_time_utc - current_time
            	#convert difference into minutes
            	minutes_difference = time_difference.total_seconds() / 60
            	#round it to nearest whole number
            	minutes_difference_rounded = round(minutes_difference)
            #sometimes "arrive" = None, so this just creates dummy data that won't light anything up
            except:
            	minutes_difference_rounded = -1
            
            if line_type == 'Tram':
                #adjust in light of walk time
                adjusted_minutes_difference = minutes_difference_rounded - tram_walk_time
            elif line_type == "U":
                adjusted_minutes_difference = minutes_difference_rounded - u_walk_time
            else: 
                print('error: productName not identified')
            

            return(adjusted_minutes_difference)

        
        #print(get_modified_departure_time(i['when'], i['line']['productName']))

        try:
            # fill up the lists
            if i['line']['name'] == 'U5':
                if i['direction'] == 'Hönow':
                    u5_eastbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                elif i['direction'] == "S+U Hauptbahnhof" or "Hauptbahnhof":
                    u5_westbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                else:
                    error_direction = i['direction']
                    print(f'unexpected U5 direction: {error_direction}')
            
            elif i['line']['name'] == 'M10':      
                if i['direction'] == 'U Turmstr.':
                    m10_northbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                elif i['direction'] == "S+U Warschauer Str.":
                    m10_southbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                else:
                    error_direction = i['direction']
                    print(f'unexpected m10 direction: {error_direction}')
            
            elif i['line']['name'] == '21':
                if i['direction'] == "S+U Lichtenberg/Gudrunstraße":
                    _21_northbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                elif i['direction'] == "S Schöneweide":
                    _21_southbound.append(get_modified_departure_time(i['when'], i['line']['productName']))
                else:
                    error_direction = i['direction']
                    print(f'unexpected 21 direction: {error_direction}')
            else:
                pass 
        except:
             print('error filling lists')
        
    print(f'u5_eastbound: {u5_eastbound}')
    print(f'u5_westbond: {u5_westbound}')
    print(f'm10_northbound: {m10_northbound}')
    print(f'm10_southbound: {m10_southbound}')
    print(f'_21_northbound: {_21_northbound}')
    print(f'_21_southbound: {_21_southbound}')

def lighter(arrival_list, line, light_1, light_2, light_3, light_4, light_5):
    #reset everything to black/off
    #pixels[light_1] = (0,0,0)
    #pixels[light_2] = (0,0,0)
    #pixels[light_3] = (0,0,0)
    #pixels[light_4] = (0,0,0)
    #pixels[light_5] = (0,0,0)


    #set the line color - create a dictionary and pull it out?
    light_color_dict = {'u5':U5_COLOR, 'm10':M10_COLOR, '_21':_21_COLOR}

    light_color = light_color_dict[line]

    # list of all of the lights so you can remove the ones that get lit
    light_list = [light_1, light_2, light_3, light_4, light_5]
    
    
    for i in arrival_list:
        if 0 <= i <= 1:
            #light the corresponding light
            pixels[light_1] = light_color
            #remove the light from the list so it does not go black
            if light_1 in light_list: light_list.remove(light_1)
        elif 2 <= i <= 3:
            pixels[light_2] = light_color
            if light_2 in light_list: light_list.remove(light_2)
        elif 4 <= i <= 7:
            pixels[light_3] = light_color
            if light_3 in light_list: light_list.remove(light_3)
        elif 8 <= i <= 12:
            pixels[light_4] = light_color
            if light_4 in light_list: light_list.remove(light_4)
        elif 13 <= i <= 20:
            pixels[light_5] = light_color
            if light_5 in light_list: light_list.remove(light_5)
        else:
            pass 
    
    #turn off any lights that don't have a corresponding value
    for i in light_list:
    	pixels[i] = (0,0,0)
       


while True:
	#try:
	#check current time
	now_time = datetime.now()
    
	# Check if the now time is between 8 AM and 10 PM
	if 8 <= now_time.hour < 22:
		#if so, run the lights
		grabber()

		lighter(u5_eastbound, 'u5', 0, 1, 2, 3, 4)
		lighter(m10_southbound, 'm10', 5, 6 ,7, 8, 9)
		lighter(_21_southbound, '_21', 10, 11, 12, 13, 14)
		lighter(u5_westbound, 'u5', 15, 16, 17, 18, 19)
		lighter(_21_northbound, '_21', 20, 21, 22, 23, 24)
		lighter(m10_northbound, 'm10', 25, 26 ,27, 28, 29)
		
		
		
		
	#if not
	else:	
		#turn them off 
		for i in range(number_of_pixels):
			pixels[i] = (0,0,0)
		print('lights out')
	
	#reset the lists for the lines
	u5_eastbound = []
	u5_westbound = []
	m10_northbound = []
	m10_southbound = []
	_21_northbound = []
	_21_southbound = []
	#except:
		#print('***************')
		#print('***ERROR*****')
		#print('*************')
		#pixels.fill(0,0,0)

	time.sleep(10)
