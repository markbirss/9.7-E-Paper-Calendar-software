#!/usr/bin/python3
# -*- coding: utf-8 -*-
#9.7 inch
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from __future__ import print_function
print('importing modules')
import glob, os
from settings import *
from icon_positions_locations import *

from PIL import Image, ImageDraw, ImageFont, ImageOps
import calendar,  pyowm
from ics import Calendar, Event
from datetime import datetime
from time import sleep
try:
    from urllib.request import urlopen
except Exception as e:
    print('It seems the network is offline :(')
    pass
import arrow
print('modules imported successfully!'+'\n')

path = '/home/pi/E-Paper-Master/Calendar/'
os.chdir(path)

EPD_WIDTH = 1200
EPD_HEIGHT = 825
font = ImageFont.truetype(path+'OpenSans-Semibold.ttf', 28)
im_open = Image.open

def main():
    while True:

        time = datetime.now()
        hour = int(time.strftime("%-H"))
        month = int(time.now().strftime('%-m'))
        year = int(time.now().strftime('%Y'))

        for i in range(1):
            print('_________Starting new loop___________'+'\n')
            
            image_name = time.strftime('%-d %b %y %H:%M')
            print('Current date:',time.strftime('%a %-d %b %y'))
            print('Current time:', time.strftime('%H:%M')+'\n')

            """Create a blank page"""
            image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)
            draw = (ImageDraw.Draw(image)).bitmap

            """image.paste the icon showing the current month"""
            image.paste(im_open(mpath+str(time.strftime("%B")+'.jpeg')), monthplace)

            """image.paste the icons with the weekday-names (Mon, Tue...) and
               image.paste a circle  on the current weekday"""
            if (week_starts_on == "Monday"):
                calendar.setfirstweekday(calendar.MONDAY)
                image.paste(weekmon, weekplace)
                draw(weekdaysmon[(time.strftime("%a"))], weekday)

            if (week_starts_on == "Sunday"):
                calendar.setfirstweekday(calendar.SUNDAY)
                image.paste(weeksun, weekplace)
                draw(weekdaysmon[(time.strftime("%a"))], weekday)

            """Using the built-in calendar function, image.paste icons for each
               number of the month (1,2,3,...28,29,30)"""
            cal = calendar.monthcalendar(time.year, time.month)
            #print(cal) #-uncomment for debugging with incorrect dates

            for i in cal[0]:
                image.paste(im_open(dpath+str(i)+'.jpeg'), positions['a'+str(cal[0].index(i)+1)])
            for i in cal[1]:
                image.paste(im_open(dpath+str(i)+'.jpeg'), positions['b'+str(cal[1].index(i)+1)])
            for i in cal[2]:
                image.paste(im_open(dpath+str(i)+'.jpeg'), positions['c'+str(cal[2].index(i)+1)])
            for i in cal[3]:
                image.paste(im_open(dpath+str(i)+'.jpeg'), positions['d'+str(cal[3].index(i)+1)])
            for i in cal[4]:
                image.paste(im_open(dpath+str(i)+'.jpeg'), positions['e'+str(cal[4].index(i)+1)])
            try:
                for i in cal[5]:
                    image.paste(im_open(dpath+str(i)+'.jpeg'), positions['f'+str(cal[5].index(i)+1)])
            except IndexError:
                pass

            """Custom function to display text on the E-Paper.
            Tuple refers to the x and y coordinates of the E-Paper display,
            with (0, 0) being the top left corner of the display."""
            def write_text(box_width, box_height, text, tuple):
                text_width, text_height = font.getsize(text)
                if (text_width, text_height) > (box_width, box_height):
                    raise ValueError('Sorry, your text is too big for the box')
                else:
                    x = int((box_width / 2) - (text_width / 2))
                    y = int((box_height / 2) - (text_height / 2))
                    space = Image.new('L', (box_width, box_height), color=255)
                    ImageDraw.Draw(space).text((x, y), text, fill=0, font=font)
                    image.paste(space, tuple)


            """ Handling Openweathermap API"""
            print("Preparing to fetch data from openweathermap API")
            owm = pyowm.OWM(api_key)
            if owm.is_API_online() is True: #test server connection
                observation = owm.weather_at_place(location)
                print("Fetching weather data...")
                weather = observation.get_weather()
                weathericon = weather.get_weather_icon_name()
                Humidity = str(weather.get_humidity())
                cloudstatus = str(weather.get_clouds())
                weather_description = (str(weather.get_status()))
                
                if units == "metric":
                    Temperature = str(int(weather.get_temperature(unit='celsius')['temp']))
                    windspeed = str(int(weather.get_wind()['speed']))
                    write_text(200, 50, Temperature + " °C", (1000, 90))
                    write_text(200, 50, windspeed+" km/h", (1000, 190))

                if units == "imperial":
                    Temperature = str(int(weather.get_temperature(unit='fahrenheit')['temp']))
                    windspeed = str(int(weather.get_wind()['speed']*0.621))
                    write_text(200, 50, Temperature + " °F", (1000, 90))
                    write_text(200, 50, windspeed+" mph", (1000, 190))

                if hours == "24":
                    sunrisetime = str(datetime.fromtimestamp(int(weather.get_sunrise_time(timeformat='unix'))).strftime('%-H:%M'))
                    sunsettime = str(datetime.fromtimestamp(int(weather.get_sunset_time(timeformat='unix'))).strftime('%-H:%M'))

                if hours == "12":
                    sunrisetime = str(datetime.fromtimestamp(int(weather.get_sunrise_time(timeformat='unix'))).strftime('%-I:%M'))
                    sunsettime = str(datetime.fromtimestamp(int(weather.get_sunset_time(timeformat='unix'))).strftime('%-I:%M'))

                print('temperature: '+Temperature +' °C')
                print('humidity: '+Humidity+'%')
                print('fetched icon code: '+weathericon)
                print('equivalent to icon: '+weathericons[weathericon]+'\n')
                print('Current wind speed: '+windspeed+ 'km/h')
                print('The sunrise today took take place place at: '+sunrisetime)
                print('The sunset today will take place place at: '+sunsettime)
                print('The current Cloud condition is: ' + cloudstatus + '%')
                print('Weather: '+ weather_description)

                """Drawing the fetched weather icon"""
                image.paste(im_open(wpath+weathericons[weathericon]+'.jpeg'), wiconplace)

                """Drawing the fetched temperature"""
                image.paste(tempicon, tempplace)
                
                """Drawing the fetched humidity"""
                image.paste(humicon, humplace)
                write_text(200, 50, Humidity + " %", (1000, 140))

                """Drawing the fetched sunrise time"""
                image.paste(sunriseicon, sunriseplace)
                write_text(200, 50, sunrisetime, (750, 140))

                """Drawing the fetched sunset time"""
                image.paste(sunseticon, sunsetplace)
                write_text(200,50, sunsettime, (750, 190))

                """Drawing the fetched wind speed"""
                image.paste(windicon, windiconspace)

                """Write a short weather description"""
                write_text(250,50, weather_description, (700, 90))

            else:
                image.paste(no_response, wiconplace)
                pass

            """Filter upcoming events from your iCalendar/s"""
            print('Fetching events from your calendar'+'\n')
            events_this_month = []
            upcoming = []
            for icalendars in ical_urls:
                decode = str(urlopen(icalendars).read().decode())
                #fix a bug related to Alarm action by replacing parts of the icalendar
                fix_e = decode.replace('BEGIN:VALARM\r\nACTION:NONE','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')
                #uncomment line below to display your calendar in ical format
                #print(fix_e)
                ical = Calendar(fix_e)
                for events in ical.events:
                    if time.now().strftime('%-m %Y') == (events.begin).format('M YYYY') and (events.begin).format('DD') >= time.now().strftime('%d'):
                        upcoming.append({'date':events.begin.format('DD MMM'), 'event':events.name})
                        events_this_month.append(int((events.begin).format('D')))
                    if month == 12:
                        if (1, year+1) == (1, int((events.begin).year)):
                            upcoming.append({'date':events.begin.format('DD MMM'), 'event':events.name})
                    if month != 12:
                        if (month+1, year) == (events.begin).format('M YYYY'):
                            upcoming.append({'date':events.begin.format('DD MMM'), 'event':events.name}) # HS sort events by date

            def takeDate(elem):
                return elem['date']

            upcoming.sort(key=takeDate)

            del upcoming[7:]
            # uncomment the following 2 lines to display the fetched events
            # from your iCalendar
            print('Upcoming events:')
            print(upcoming)

            #Credit to Hubert for suggesting truncating event names
            def write_text_left(box_width, box_height, text, tuple):
                text_width, text_height = font.getsize(text)
                while (text_width, text_height) > (box_width, box_height):
                    text=text[0:-1]
                    text_width, text_height = font.getsize(text)
                y = int((box_height / 2) - (text_height / 2))
                space = Image.new('L', (box_width, box_height), color=255)
                ImageDraw.Draw(space).text((0, y), text, fill=0, font=font)
                image.paste(space, tuple)

            """Write event dates and names on the E-Paper"""
            for dates in range(len(upcoming)):
                write_text(100, 40, (upcoming[dates]['date']), date_positions['d'+str(dates+1)])

            for events in range(len(upcoming)):
                write_text_left(520, 40, (upcoming[events]['event']), event_positions['e'+str(events+1)])

            """Draw circles on any days which include an Event"""
            for x in events_this_month:
                if x in cal[0]:
                    draw(positions['a'+str(cal[0].index(x)+1)], eventicon)
                if x in cal[1]:
                    draw(positions['b'+str(cal[1].index(x)+1)], eventicon)
                if x in cal[2]:
                    draw(positions['c'+str(cal[2].index(x)+1)], eventicon)
                if x in cal[3]:
                    draw(positions['d'+str(cal[3].index(x)+1)], eventicon)
                if x in cal[4]:
                    draw(positions['e'+str(cal[4].index(x)+1)], eventicon)
                try:
                    if x in cal[5]:
                        draw(positions['f'+str(cal[5].index(x)+1)], eventicon)
                except IndexError:
                    pass

            """image.paste a square with round corners on today's date"""
            today = time.day
            if today in cal[0]:
                draw(positions['a'+str(cal[0].index(today)+1)], dateicon)
            if today in cal[1]:
                draw(positions['b'+str(cal[1].index(today)+1)], dateicon)
            if today in cal[2]:
                draw(positions['c'+str(cal[2].index(today)+1)], dateicon)
            if today in cal[3]:
                draw(positions['d'+str(cal[3].index(today)+1)], dateicon)
            if today in cal[4]:
                draw(positions['e'+str(cal[4].index(today)+1)], dateicon)
            try:
                if today in cal[5]:
                    draw(positions['f'+str(cal[0].index(today)+1)], dateicon)
            except IndexError:
                    pass

            # Save the generated image in the E-Paper-folder.
            print('saving the generated image now...')
            image.save(str(image_name)+'.jpeg')
            print('image saved successfully')

            # delete the list so deleted events can be removed from the list
            del events_this_month[:]
            del upcoming[:]
            
            for i in range(1):
                nexthour = ((60 - int(time.strftime("%-M")))*60) - (int(time.strftime("%-S")))
                sleep(nexthour)

if __name__ == '__main__':
    main()
