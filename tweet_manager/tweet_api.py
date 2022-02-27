
from dateutil import parser


from time import sleep
import requests
from requests.exceptions import ConnectionError
import re
raw_headers="""Accept: */*
User-Agent: Thunder Client (https://www.thunderclient.com)
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAMWiVgEAAAAAS3oPA4Am9dY39s3b0L%2Fhke5im4I%3DeocuZgNNtGQz2R2oQstPfRWoPB27lDIreMaswLZhn69p7feng1"""

# Support the sections of ISO 8601 date representation that are accepted by
# timedelta

def get_headers_as_dict(headers: str):
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic
headers = get_headers_as_dict(headers=raw_headers)

def get_date(tweet_id):
    
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=created_at"

    payload={}
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data=payload)

            data = response.json()
            print(data)
            
        
            date = parser.isoparse(data['data']['created_at'])
            print(date)
            return date

        except ConnectionError as e:
            print(e)
            print("connection error at >>TWEET DATE FETCHING<<")
            sleep(1)