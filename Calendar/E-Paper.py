#!/usr/bin/python3
# -*- coding: utf-8 -*-
# For 9.7 inch E-Paper
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from __future__ import print_function
import glob, os
from settings import *
from icon_positions_locations import *
import random
import gc
from PIL import Image, ImageDraw, ImageFont, ImageOps
import calendar,  pyowm
from ics import Calendar, Event
from datetime import datetime, date, timedelta
from time import sleep
try:
    from urllib.request import urlopen
except Exception as e:
    print('It seems the network is offline :(')
    pass

try:
    import feedparser
except ImportError:
    print("Please install feedparser with: sudo pip3 install feedparser")
    print("and")
    print("pip3 install feedparser")

#import arrow
#print('modules imported successfully!'+'\n')

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
        mins = int(time.strftime("%M"))
        seconds = int(time.strftime("%S"))

        for i in range(1):
            """At the following hours (midnight, midday and 6 pm), perform
               a calibration of the display's colours"""
            #if hour is 0 or hour is 12 or hour is 18:
                #image.paste(im_open(opath+'white.jpeg'))
            print('_________Starting new loop___________'+'\n')

            image_name = 'current-image'
            print('Date:', time.strftime('%a %-d %b %y')+', Time: '+time.strftime('%H:%M')+'\n')

            """Create a blank white page first"""
            image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)
            draw = (ImageDraw.Draw(image)).bitmap

            """Add the icon with the current month's name"""
            image.paste(im_open(mpath+str(time.strftime("%B")+'.jpeg')), monthplace)

            """Add weekday-icons (Mon, Tue...) and draw a circle on the
            current weekday"""
            if (week_starts_on == "Monday"):
                calendar.setfirstweekday(calendar.MONDAY)
                image.paste(weekmon, weekplace)
                draw(weekdaysmon[(time.strftime("%a"))], weekday)

            """For those whose week starts on Sunday, change accordingly"""
            if (week_starts_on == "Sunday"):
                calendar.setfirstweekday(calendar.SUNDAY)
                image.paste(weeksun, weekplace)
                draw(weekdaysmon[(time.strftime("%a"))], weekday)

            """Using the built-in calendar function, add icons for each
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
            if len(cal) is 6:
                for i in cal[5]:
                    image.paste(im_open(dpath+str(numbers)+'.jpeg'), positions['f'+str(cal[5].index(numbers)+1)])

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


            """Connect to Openweathermap API to fetch weather data"""
            print("Connecting to Openweathermap API servers...")
            owm = pyowm.OWM(api_key)
            if owm.is_API_online() is True:
                observation = owm.weather_at_place(location)
                print("weather data:")
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

                print('Temperature: '+Temperature+' °C')
                print('Humidity: '+Humidity+'%')
                #print('Icon code: '+weathericon)
                print('weather-icon name: '+weathericons[weathericon])
                print('Wind speed: '+windspeed+'km/h')
                print('Sunrise-time: '+sunrisetime)
                print('Sunset time: '+sunsettime)
                print('Cloudiness: ' + cloudstatus+'%')
                print('Weather description: '+weather_description+'\n')

                """Add the weather icon"""
                image.paste(im_open(wpath+weathericons[weathericon]+'.jpeg'), wiconplace)

                """Add the temperature icon at it's position"""
                image.paste(tempicon, tempplace)

                """Add the humidity icon and display the humidity"""
                image.paste(humicon, humplace)
                write_text(200, 50, Humidity + " %", (1000, 140))

                """Add the sunrise icon and display the sunrise time"""
                image.paste(sunriseicon, sunriseplace)
                write_text(200, 50, sunrisetime, (750, 140))

                """Add the sunset icon and display the sunset time"""
                image.paste(sunseticon, sunsetplace)
                write_text(200,50, sunsettime, (750, 190))

                """Add the wind icon at it's position"""
                image.paste(windicon, windiconspace)

                """Add a short weather description"""
                write_text(250,50, weather_description, (700, 90))

            else:
                image.paste(no_response, wiconplace)
                pass

            """Algorithm for filtering and sorting events from your
            iCalendar/s"""
            print('Fetching events from your calendar'+'\n')
            events_this_month = []
            upcoming = []
            today = date.today()

            """Create a time span using the events_max_range value (in days)
            to filter events in that range"""
            time_span = today + timedelta(days=int(events_max_range))

            for icalendars in ical_urls:
                decode = str(urlopen(icalendars).read().decode())
                fix_e_1 = decode.replace('BEGIN:VALARM\r\nACTION:NONE','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')
                fix_e_2 = fix_e_1.replace('BEGIN:VALARM\r\nACTION:EMAIL','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')
                #uncomment line below to display your calendar in ical format
                #print(fix_e_2)
                ical = Calendar(fix_e_2)
                for events in ical.events:
                    if events.begin.date().month == today.month:
                        if int((events.begin).format('D')) not in events_this_month:
                            events_this_month.append(int((events.begin).format('D')))
                    if today <= events.begin.date() <= time_span:
                        upcoming.append({'date':events.begin.format('YYYY MM DD'), 'event':events.name})

            def takeDate(elem):
                return elem['date']

            upcoming.sort(key=takeDate)

            del upcoming[7:]

            #print('Upcoming events:',upcoming) #Display fetched events

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
                readable_date = datetime.strptime(upcoming[dates]['date'], '%Y %m %d').strftime('%-d %b')
                write_text(100, 40, readable_date, date_positions['d'+str(dates+1)])

            for events in range(len(upcoming)):
                write_text_left(540, 40, (upcoming[events]['event']), event_positions['e'+str(events+1)])

            """Add rss-feeds at the bottom section of the Calendar"""
            def multiline_text(text, max_width):
                lines = []
                if font.getsize(text)[0] <= max_width:
                    lines.append(text)
                else:
                    words = text.split(' ')
                    i = 0
                    while i < len(words):
                        line = ''
                        while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                            line = line + words[i] + " "
                            i += 1
                        if not line:
                            line = words[i]
                            i += 1
                        lines.append(line)
                return lines

            rss_feed = []
            for feeds in rss_feeds:
                text = feedparser.parse(feeds)
                for posts in text.entries:
                    rss_feed.append(posts.title)

            random.shuffle(rss_feed)
            news = []

            if len(cal) == 5:
                del rss_feed[4:]

            if len(cal) == 6:
                del rss_feed[2:]

            for title in range(len(rss_feeds)):
                news.append(multiline_text(rss_feed[title], 1200))

            news = [j for i in news for j in i]

            if len(cal) is 5:
                if len(news) > 5:
                    del news[4:]
                for lines in range(len(news)):
                    write_text_left(1200, 40, news[lines], rss_places['line_'+str(lines+1)])

            if len(cal) is 6:
                if len(news) > 3:
                    del news[2:]
                for lines in range(len(news)):
                    write_text_left(1200, 40, news[lines], rss_places['line_'+str(lines+1)])

            """Draw smaller squares on days with events"""
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
                if len(cal) is 6:
                    if x in cal[5]:
                         draw(positions['f'+str(cal[5].index(x)+1)], eventicon)


            """Draw a larger square on today's date"""
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
            if len(cal) is 6:
                if today in cal[5]:
                    draw(positions['f'+str(cal[5].index(today)+1)], dateicon)

            # Save the generated image in the E-Paper-folder.
            print('Saving the generated image now...')
            image.save(str(image_name)+'.bmp')
            print('Image saved successfully')
            print('______Sleeping until the next loop______'+'\n')

            # delete the list so deleted events can be removed from the list
            del events_this_month
            del upcoming
            del rss_feed
            del news
            gc.collect()

            for i in range(1):
                nexthour = ((60 - int(time.strftime("%-M")))*60) - (int(time.strftime("%-S")))
                sleep(nexthour)

if __name__ == '__main__':
    main()
