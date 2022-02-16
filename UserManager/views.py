# for converting the dict to queryString
import json
from urllib.parse import urlencode

from rest_framework.decorators import api_view
# for fetching the users from twitter
import requests

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
# Create your views here.



# header 

raw_headers="""Accept: */*
User-Agent: Thunder Client (https://www.thunderclient.com)
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAMWiVgEAAAAAS3oPA4Am9dY39s3b0L%2Fhke5im4I%3DeocuZgNNtGQz2R2oQstPfRWoPB27lDIreMaswLZhn69p7feng1"""

def get_headers_as_dict(headers: str) -> dict:
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic
headers = get_headers_as_dict(headers=raw_headers)
# Create your views here.
@api_view(['GET','POST','PUT','PATCH','DELETE'])

def TwitterUserManager(request):
    if request.method == 'GET':

        query =  request.query_params

        url = "https://api.twitter.com/2/users/by"

        query_string = urlencode(query=query)

        url = url + "?"+ query_string + "&" + "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld";

        payload={}

        response = requests.request("GET", url, headers=headers, data=payload)

        response = JSONRenderer().render(response)

        return Response(data=response,content_type="application/json")
        
