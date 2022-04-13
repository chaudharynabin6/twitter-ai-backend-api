import re
 
# https://catriscode.com/2021/05/01/tweets-cleaning-with-python/
def clean_tweet(tweet):
    temp = tweet.lower()
    # temp = re.sub("'", "", temp) # to avoid removing contractions in english
    # Removing hashtags and mentions
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    # Removing links
    temp = re.sub(r'http\S+', '', temp)
    # Removing punctuations
    # temp = re.sub('[()!?]', ' ', temp)
    # temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)

    return temp