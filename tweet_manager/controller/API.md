# API help

# get_tweets(id:int,pagination_token : str=next_token)
# get_tweets(id:int)
```json
{'data': [{'id': '1468938104446894092',
           'text': '@Rainmaker1973 Shanghai is beautiful'},
          {'id': '1468840273849589762',
           'text': '@PPathole Probably way sooner before it’s too hot for '
                   'civilization'},
          {'id': '1468704295898038273',
           'text': 'RT @SpaceX: All systems and weather are looking good ahead '
                   'of tonight’s launch of IXPE for @NASA '
                   'https://t.co/bJFjLCzWdK https://t.co/tCYnB…'},
          {'id': '1468689628161052674',
           'text': 'Unless susceptible to extreme natural disasters, nuclear '
                   'power plants should not be shut down'},
          {'id': '1468687890376970257',
           'text': '@WatcherGuru Taxing all billionaires at 100% only drops '
                   'national debt by ~10%, which is just one year of deficit '
                   'spending'},
          {'id': '1468687495084847115',
           'text': '@WatcherGuru This is scary, something’s got to give'},
          {'id': '1468685877970935809',
           'text': 'Nothing is more permanent than a “temporary” government '
                   'program'},
          {'id': '1468685150942908424', 'text': '@traderjourney Exactly!'},
          {'id': '1468685044239814666',
           'text': 'There is a lot of accounting trickery in this bill that '
                   'isn’t being disclosed to the public'},
          {'id': '1468684576407101440',
           'text': 'If “temporary” provisions in the Build Back Better Act '
                   'become permanent, US national debt will increase by 24%! '
                   'https://t.co/kKdpc45JoB'}],
 'meta': {'newest_id': '1468938104446894092',
          'next_token': '7140dibdnow9c7btw3z3b2647ln50kjowud35zhaku2i8',
          'oldest_id': '1468684576407101440',
          'result_count': 10}}
```

# here important data are 

by default there is twitter_id and and all information in twitter_user table


meta.next_token --> used as pagination_token

forr item in data : 
        {id,text} = item

id --> twitter id
text --> tweet text

# get_user_detail(screen_name:str)

```json
{'contributors_enabled': False,
 'created_at': 'Tue Jun 02 20:12:29 +0000 2009',
 'default_profile': False,
 'default_profile_image': False,
 'description': '',
 'entities': {'description': {'urls': []}},
 'favourites_count': 11202,
 'follow_request_sent': False,
 'followers_count': 65813945,
 'following': True,
 'friends_count': 108,
 'geo_enabled': False,
 'has_extended_profile': True,
 'id': 44196397,
 'id_str': '44196397',
 'is_translation_enabled': False,
 'is_translator': False,
 'lang': None,
 'listed_count': 82388,
 'location': '',
 'name': 'Elon Musk',
 'notifications': False,
 'profile_background_color': 'C0DEED',
 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png',
 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png',
 'profile_background_tile': False,
 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/44196397/1576183471',
 'profile_image_url': 'http://pbs.twimg.com/profile_images/1442634650703237120/mXIcYtIs_normal.jpg',
 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1442634650703237120/mXIcYtIs_normal.jpg',
 'profile_link_color': '0084B4',
 'profile_location': None,
 'profile_sidebar_border_color': 'C0DEED',
 'profile_sidebar_fill_color': 'DDEEF6',
 'profile_text_color': '333333',
 'profile_use_background_image': True,
 'protected': False,
 'screen_name': 'elonmusk',
 'status': {'contributors': None,
            'coordinates': None,
            'created_at': 'Thu Dec 09 13:38:30 +0000 2021',
            'entities': {'hashtags': [],
                         'symbols': [],
                         'urls': [],
                         'user_mentions': [{'id': 177101260,
                                            'id_str': '177101260',
                                            'indices': [0, 14],
                                            'name': 'Massimo',
                                            'screen_name': 'Rainmaker1973'}]},
            'favorite_count': 3866,
            'favorited': False,
            'geo': None,
            'id': 1468938104446894092,
            'id_str': '1468938104446894092',
            'in_reply_to_screen_name': 'Rainmaker1973',
            'in_reply_to_status_id': 1468935968480653315,
            'in_reply_to_status_id_str': '1468935968480653315',
            'in_reply_to_user_id': 177101260,
            'in_reply_to_user_id_str': '177101260',
            'is_quote_status': False,
            'lang': 'in',
            'place': None,
            'retweet_count': 164,
            'retweeted': False,
            'source': '<a href="http://twitter.com/download/iphone" '
                      'rel="nofollow">Twitter for iPhone</a>',
            'text': '@Rainmaker1973 Shanghai is beautiful',
            'truncated': False},
 'statuses_count': 16266,
 'time_zone': None,
 'translator_type': 'none',
 'url': None,
 'utc_offset': None,
 'verified': True,
 'withheld_in_countries': []}
```