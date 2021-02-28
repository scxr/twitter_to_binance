import json
import tweepy
import time
import requests
from monitor_price_change import main_loop
from thread_pool_manager import ThreadPool
pool = ThreadPool(20)
with open("credentials.json") as f:
    credentials = json.load(f)
last_id = 1300000000000000000
twitter_name = "Bitc0inBar0n"

auth = tweepy.OAuthHandler(credentials["API_KEY"], credentials["API_SECRET"])
auth.set_access_token(credentials["ACCESS_TOKEN"], credentials["ACCESS_SECRET"])
api = tweepy.API(auth)

def alert_via_discord(user:str, crypto:str, full_tweet:str) -> None:
    hook = "https://discord.com/api/webhooks/812677344790577212/qbQZjSbbXLY9UyXHRZVUGaR2VAQYQyDGshglDzmnvHFr8VdwVXP5Rdb6QDVkJnTKKKPO"
    requests.post(hook, data={"content":f"{user} tweeted about {crypto}\nFull tweet: {full_tweet}", "username":"twitter_to_discord"})

cryptos_to_check = {
    "bitcoin":"BTC",
    "ethereum":"ETH",
    "doge":"DOGE"
}
tweets = []
users_to_monitor = ["Bitc0inBar0n","elonmusk"]
def setup_dict(users):
    my_dict = {}
    for i in users:
        my_dict[i] = 1300000000000000000
    return my_dict
last_tweets=setup_dict(users_to_monitor)
print(last_tweets)
found_in = []
while 1:
    for user in users_to_monitor:
        tweets = api.user_timeline(screen_name = user,
                                count = 1,
                                include_rts = False,
                                tweet_mode='extended',
                                since_id = last_id
                                )
        for i in tweets:
            if i.id > last_tweets[user]:
                print("New tweet : ", i.full_text)
                last_tweets[user] = i.id
                for j in cryptos_to_check.keys():
                    if j in i.full_text.lower(): 
                        pool.add_task(main_loop, j)
                        pool.wait_completion()
                        alert_via_discord(user, j, i.full_text)
                        found_in.append(i.id)
                for j in cryptos_to_check.values():
                    if j.lower() in i.full_text.lower() and i.id not in found_in:
                        pool.add_task(main_loop, j)
                        pool.wait_completion()
                        alert_via_discord(user, j, i.full_text)
    print("sleeping")
    time.sleep(10)