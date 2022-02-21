# for converting the dict to queryString

import json
from urllib.parse import urlencode
from django.http import JsonResponse

# for fetching the users from twitter
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



# Application imports
from . import serializers
from .import models
# Create your views here.



# header 

raw_headers="""Accept: */*
User-Agent: Thunder Client (https://www.thunderclient.com)
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAMWiVgEAAAAAS3oPA4Am9dY39s3b0L%2Fhke5im4I%3DeocuZgNNtGQz2R2oQstPfRWoPB27lDIreMaswLZhn69p7feng1"""

def get_headers_as_dict(headers: str):
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic
headers = get_headers_as_dict(headers=raw_headers)
# Create your views here.
@api_view(['GET','PATCH'])

def search_and_add_twitter_users(request,users=""):
    if request.method == 'GET':

        query =  request.query_params

        url = "https://api.twitter.com/2/users/by/?usernames="

        query_string = urlencode(query=query)

        url = url + users+ "&" + "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld";

        payload={}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        if users == "":
            all_users = models.TwitterUser.objects.filter(isAnalysing=True)
            serialized_users = serializers.TwitterUserSerializer(all_users,many=True)
            data = serialized_users.data

        return Response(data=data)


    # if request.method == 'POST':

    #     print(request.data)
    #     all_users = models.TwitterUser.objects.all()
    #     serialized_users = serializers.TwitterUserSerializer(data=request.data)
        
    #     if serialized_users.is_valid():
    #         serialized_users.save()
    #         print(serialized_users.validated_data)
    #         return Response(request.data,status=status.HTTP_201_CREATED);
        
    #     return Response(data={'msg':serialized_users.errors},status=status.HTTP_400_BAD_REQUEST)


    

    if request.method == 'PATCH':

        request_users = request.data
        
        # print(type(request_users))
        # print(request_users[0])

        errors = []
        updated_users = []
        for user in request_users:
            db_user,_ = models.TwitterUser.objects.get_or_create(id=user.get('user_id'))
            print(db_user)
            serialized_users = serializers.TwitterUserSerializer(instance=db_user,data=user,partial=True)

            if serialized_users.is_valid():
                serialized_users.save()
                updated_users.append(serialized_users.data)
            
            if serialized_users.errors:
                errors.append(
                    {
                        'user_id':user.get('user_id'),
                        'error':serialized_users.errors
                    }
                )
        data = {"updated": request_users,"error":errors}
        return JsonResponse(data=data,status=status.HTTP_200_OK,safe=False)