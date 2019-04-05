import requests
from bs4 import BeautifulSoup
if __name__ == ' __main__':
    all_tweets = []
    url = 'https://twitter.com/search?q=tech%20breakup&src=typd'
    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')
    print(html)
    timeline = html.select('#stream li.stream-item')
    for tweet in timeline:
        tweet_id = tweet['data-item-id']
        tweet_text = tweet.select('p.tweet-text')[0].get_text()
        all_tweets.append({"id": tweet_id, "text": tweet_text})
        # print(all_tweets)
for i in all_tweets:
    print(i)
# print(all_tweets)
print(all_tweets)
