# Import libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import tweepy
import os
import csv
import geojson
import configparser
from geopy.geocoders import Nominatim
import urllib.request

# 0 for history, 1 for streaming

# Function to read the config file
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config.get('Tweet','ckey')
    consumer_secret = config.get('Tweet','csecret')
    access_token = config.get('Tweet','atoken')
    access_token_secret = config.get('Tweet','asecret')
    location = config.get('Location', 'place')
    keyword = config.get('Keyword', 'search_word')
    range = config.get('Range', 'kilometers')
    since = config.get('Since', 'since')
    geocoder_key = config.get('Geo_key', 'geo_key')
    mode = config.get('HistoryOrStream', 'selectmode')

    return consumer_key, consumer_secret, access_token, access_token_secret, location, keyword, range, since, geocoder_key, mode

# Loads the values from the function to variables
ckey, csecret, atoken, asecret, search_location, search_word, range_dist, since_date, geocode_key, extraction_mode = read_config("E:/config/twphotos.cfg.txt")

# Library geopy used to get lat-long from the place of the name
geolocator = Nominatim(user_agent=geocode_key, timeout=5)
location = geolocator.geocode(search_location)
latitude = (location.latitude)
longitude = (location.longitude)

# Printing to test if everything is correct
print(search_word)
print([search_word])
print(since_date)
print(search_location)
print(range_dist)
print(geocode_key)
print(location)
print(latitude)
print(longitude)
print(extraction_mode)

# Extraction mode is 0 or 1. 0 is to get past tweets. 1 is to stream tweets i.e get live tweets.
extraction_mode = extraction_mode


# Authentication of twitter
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


# Extraction mode 0 hence get tweets from the past.
if extraction_mode == '0':

    # Count mentioned to check number of tweets captured
    count = 0

    # For getting past 7 days tweets
    # Cursor in tweepy to get past tweets.
    for tweet in tweepy.Cursor(api.search, q=search_word, since=since_date, lang='en', tweet_mode='extended',
                               geocode='{},{},{}'.format(34.8021,38.9968,range_dist)
                               ).items():
        time.sleep(2)


        # Opening a file to save the collected tweets
        with open('E:/Outputs/images_output/ipl.csv', 'a', encoding='utf-8', newline='') as f_output_history:
            csv_file_history = csv.writer(f_output_history)

            # To avoid column names being printed again, file size is checked. Column names will be printed only if file is empty
            # else column names will not be printed
            file_is_empty = os.stat('E:/Outputs/images_output/ipl.csv').st_size == 0
            if file_is_empty:
                csv_file_history.writerow(['Tweet', 'Time_Created', 'Location', 'Lat_Long', 'ID', 'Images'])

            print(tweet)

            # Gets the text from the tweet
            try:
                tweet_text = tweet.full_text
            except Exception as e:
                tweet_text = None
            print('Tweet:', tweet_text)


            # Time the tweet was created
            try:
                created = tweet.created_at
            except Exception as e:
                created = None
            print('Created:', created)


            # Location name of the user
            try:
                location = tweet.user.location
            except Exception as e:
                location = None
            print('Location:', location)

            # Location coordinates of the user
            try:
                co_ordinates = tweet.coordinates
            except Exception as e:
                co_ordinates = None
            print('Co ordinates', co_ordinates)

            # Tweet id. Can check if same tweet has been downloaded twice.
            try:
                id = tweet.id
            except Exception as e:
                id = None
            print('ID', id)


            try:
                images = tweet.entities
                for key in images:
                    print("keys ...",key)
                    if key == "media":
                        #print('here printing images- entities', key(images))
                        #print('here printing images- user mentions', images["user_mentions"][0]['screen_name'])
                        print('images_url', images["media"][0]['media_url'])
            except Exception as e:
                print("Exception raised",e)
                images=None

            #
            # def dl_img(url, file_path, file_name):
            #     full_path = ('E:/images_output/download/' + file_name + '.jpg')
            #     urllib.request.urlretrieve(url, full_path)
            #
            #
            # url = input('Enter the url:')
            # file_name = input('Enter the file name:')
            #
            # dl_img(url, 'download/', file_name)


            csv_file_history.writerow([tweet_text, created, location, co_ordinates, id, images])

        count = count+1
        print("Count:", count)
        print("--------")


# Extraction mode 1. Hence it is streaming or getting live tweets
elif extraction_mode == '1':
    import time

    # Class to get live tweets
    class MyListner(StreamListener):

        def on_data(self, data):

            # Load tweet in json format
            tweet = json.loads(data)

            # To avoid column names being printed again, file size is checked. Column names will be printed only if file is empty
            # else column names will not be printed
            with open('E:/Outputs/images_output/ipl.csv', 'a', encoding='utf-8', newline='') as f_output_stream:
                csv_file_stream = csv.writer(f_output_stream)
                file_is_empty = os.stat('E:/Outputs/images_output/ipl.csv').st_size==0
                if file_is_empty:
                    csv_file_stream.writerow(['tweet', 'time_created', 'location', 'coordinates', 'id','Images'])

                # Get text from the tweet
                try:
                    tweet_text = tweet['text']
                except Exception as e:
                    tweet_text = None
                print("Tweet:", tweet_text)

                # Get location of the user
                try:
                    location = tweet['user']['location']
                except Exception as e:
                    location = None
                print("Location:", location)

                # Time the time the tweet was created by the user
                try:
                    time_created = tweet['created_at']
                except Exception as e:
                    time_created = None
                print("Time:", time_created)

                # get the id so as to delete duplicate tweets
                try:
                    id = tweet['id']
                except Exception as e:
                    id = None
                print("ID:", id)

                # get coordinates of the user
                try:
                    coordinates = tweet['coordinates']
                except Exception as e:
                    coordinates = None
                print("Coordinates:", coordinates)

                try:
                    images = tweet.entities
                    for key in images:
                        print("keys ...", key)
                        if key == "media":
                            # print('here printing images- entities', key(images))
                            # print('here printing images- user mentions', images["user_mentions"][0]['screen_name'])
                            print('images_url', images["media"][0]['media_url'])
                except Exception as e:
                    print("Exception raiseSd", e)
                    images = None


                csv_file_stream.writerow([tweet_text, time_created, location, coordinates, id, images])

                # count = count + 1
                #     print("Count:", count)
                print("-----------------")
                time.sleep(2)


        def on_error(self, status):
            print(status)

    twitterStream = Stream(auth, MyListner())
    twitterStream.filter(track=[search_word], languages=['en'])



