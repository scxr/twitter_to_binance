# todo
# fix amount to buy for alt and main coins
import json
import tweepy
import time
import requests
import sys
import math
from monitor_price_change import main_loop, get_price
from thread_pool_manager import ThreadPool
from get_binance_balance import get_balance, get_tick_size, get_alt_tick_size

def setup_dict(users):
    my_dict = {}
    for i in users:
        my_dict[i] = (1300000000000000000,0)
    return my_dict

balance, amnt ,can_use = get_balance()
can_use = True
users_to_monitor = ["Bitc0inBar0n","elonmusk"]
mydict=setup_dict(users_to_monitor)
if can_use:
    print(f'{balance} USDT')
    to_use = input('How much of this balance would you like to use? : (in percentage)')
    amount_to_play_with = float(amnt) * (float(to_use)/100)
    distribute_or_no = input('Would you like to distribute this amongst your users? : ')
    if distribute_or_no[0].lower() == 'y':
        to_use = 0
        to_use_total = 0
        for user in users_to_monitor:
            to_use = float(input(f'How much would you like to use for : {user}? (Total left : {100-to_use_total}) '))
            mydict[user] = (1300000000000000000, to_use)
            to_use_total += to_use
            if to_use_total > 100:
                print('You exceeded using 100%, exiting')
                sys.exit(1)
    else:
        big_boy = input(f'You selected no, who would you like to spend 100% of your balance on? Your options : {" ,".join(users_to_monitor)} : ')
        resp = (1300000000000000000, 100)
        if big_boy in mydict.keys():
            mydict[big_boy] = resp
        else:
            print('Invalid user')
            sys.exit(1)
else:
    print(balance)
    sys.exit()
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

#print(mydict)
found_in = []
while 1:
    for user in users_to_monitor:
        #print(mydict[user][1])
        #print(type(amnt))
        #print(mydict[user][1])
        amount_for_user = float(amnt) * (float(mydict[user][1])/100)
        #print(amount_for_user)
        tweets = api.user_timeline(screen_name = user,
                                count = 1,
                                include_rts = False,
                                tweet_mode='extended',
                                since_id = last_id
                                )
        for i in tweets:
            if i.id > mydict[user][0]:
                #print("New tweet : ", i.full_text)
                tmp = (i.id, mydict[user][1])
                mydict[user] = tmp
                #print(amount_for_user, amnt)
                for j in cryptos_to_check.keys():
                    if j in i.full_text.lower(): 
                        if not mydict[user][1] == 0: 
                            cryptos_price = float(get_price(j)[1])
                            cryptos_ticker = get_alt_tick_size(j.upper())
                            amount_to_buy = math.floor(
                                amount_for_user * 10 ** cryptos_ticker
                                / cryptos_price
                            ) / float(10 ** cryptos_ticker)


                            #amount_to_buy = amnt / cryptos_price - ((cryptos_price/95))
                            #amount_to_buy_dec_split = str(amount_to_buy).split('.')
                            #amount_to_buy_dec = [str(amount_to_buy_dec_split[1])[0:cryptos_ticker] if len(str(amount_to_buy_dec_split[1])) > cryptos_ticker else str(amount_to_buy_dec)][0]
                            #amount_to_buy = float('.'.join([amount_to_buy_dec_split[0],amount_to_buy_dec])) 
                            #print(amount_to_buy)
                            print(f'Buying {j}  {amount_to_buy}  {cryptos_price}')
                            pool.add_task(main_loop, j,float(amount_to_buy))
                            pool.wait_completion()
                        #alert_via_discord(user, j, i.full_text)
                        found_in.append(i.id)
                for j in cryptos_to_check.values():
                    if j.lower() in i.full_text.lower() and i.id not in found_in:
                        if not mydict[user][1] == 0:
                            cryptos_price = float(get_price(j.upper()))
                            cryptos_ticker = get_alt_tick_size(j.upper())
                            #amount_to_buy = amnt / cryptos_price - ((cryptos_price/95))
                            #amount_to_buy_dec_split = str(amount_to_buy).split('.')
                            #amount_to_buy_dec = [str(amount_to_buy_dec_split[1])[0:cryptos_ticker] if len(str(amount_to_buy_dec_split[1])) > cryptos_ticker else str(amount_to_buy_dec)][0]
                            #amount_to_buy = float('.'.join([amount_to_buy_dec_split[0],amount_to_buy_dec]))
                            amount_to_buy = math.floor(
                                amount_for_user * 10 ** cryptos_ticker
                                / cryptos_price
                            ) / float(10 ** cryptos_ticker)
                            
                            print(f'Buying {j}  {amount_to_buy}  {cryptos_price}')
                            pool.add_task(main_loop, j,amount_to_buy)
                            pool.wait_completion()
            print(i)
                        #alert_via_discord(user, j, i.full_text)
    #print("sleeping")
    time.sleep(10)