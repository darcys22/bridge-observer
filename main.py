#! python3
import config
import bs4
import multiprocessing
import os
import signal
import psutil
import requests
import telebot
import time
from web3 import Web3
# from telebot import types
# from telebot import util

bot = telebot.TeleBot(config.TgBotAPIKey)
w3 = Web3(Web3.HTTPProvider(config.ethereumHTTPProvider))

# ------------------- Query Main Page up ------------------------
def checkMainPage():
    page = requests.get(config.mainSite)
    available = False
    raw = bs4.BeautifulSoup(page.text, 'html.parser')
    if (raw.title is not None):
        available = (raw.title.string == config.titleString)
    return available

# ------------------- Query api up ------------------------
def checkBackendAPI():
    r = requests.get(url = config.apiRequest)
    response = r.status_code
    available = response == 200
    return available

# ------------------- Query wOxen Balance ------------------------
def checkTokenBalance():
    url_eth = "https://api.etherscan.io/api"
    API_ENDPOINT = url_eth+"?module=contract&action=getabi&address="+str(config.contractAddress)
    r = requests.get(url = API_ENDPOINT)
    response = r.json()
    instance = w3.eth.contract(
        address=Web3.toChecksumAddress(config.contractAddress),
        abi = response["result"]
    )
    balance = instance.functions.balanceOf(Web3.toChecksumAddress(config.hotWalletAddress)).call() / 10**config.decimals
    return balance > config.lowBalanceThreshold

# ------------------- Query Eth Balance ------------------------
def checkEthBalance():
    balance = w3.eth.get_balance(Web3.toChecksumAddress(config.hotWalletAddress)) / 10**18
    return balance > config.lowEthThreshold

# ------------------- Telegram Bot ------------------------

# Start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "I'm here to monitor your page")
# /Start

# UserID
@bot.message_handler(commands=['userid', 'UserID'])
def add_user(message):
    print(message.chat.id)
    bot.reply_to(message, "UserID = "+str(message.chat.id))
# /UserID


# Alerts checking bridge
def AlertsNotifications():
  td = 0
  while True:
    if td == 1200:
      td = 0
      # Check main page running
      try:
        mainpageAvailable = checkMainPage()
        for user in config.tg:
            if not mainpageAvailable:
                for user in config.tg:
                    bot.send_message(user, "Main Page Unavailable")
      except:
        for user in config.tg:
            bot.send_message(user, "Main Page Unavailable")
      # Check Backend API running
      try:
        APIAvailable = checkBackendAPI()
        for user in config.tg:
            if not APIAvailable:
                for user in config.tg:
                    bot.send_message(user, "API Unavailable")
      except:
        for user in config.tg:
            bot.send_message(user, "API Unavailable")

      # Check token balance
      try:
        tokenBalanceSufficient = checkTokenBalance()
        for user in config.tg:
            if not tokenBalanceSufficient:
                for user in config.tg:
                    bot.send_message(user, "wOxen Hotwallet Balance Low")
      except:
        for user in config.tg:
            bot.send_message(user, "wOxen check Unavailable")

      # Check Eth balance
      try:
        ethBalanceSufficient = checkEthBalance()
        for user in config.tg:
            if not ethBalanceSufficient:
                for user in config.tg:
                    bot.send_message(user, "Eth Hotwallet Balance Low")
      except:
        for user in config.tg:
            bot.send_message(user, "Eth check Unavailable")

    time.sleep(1200)
    td += 1200
#

# Test Alerts checking bridge - will only check the main page of the bridge and more frequently (12 seconds)
def TestNotifications():
  td = 0
  while True:
    if td == 12:
      td = 0
      # Check main page running
      try:
        mainpageAvailable = checkMainPage()
        for user in config.tg:
            if not mainpageAvailable:
                for user in config.tg:
                    bot.send_message(user, "Main Page Unavailable")
      except:
        for user in config.tg:
            bot.send_message(user, "Main Page Unavailable")

    time.sleep(12)
    td += 12
#

# ------------------- Misc ------------------------

# Except proc kill
def kill(proc_pid = os.getpid(), sig=signal.SIGTERM):
  process = psutil.Process(proc_pid)
  for proc in process.children(recursive=True):
    proc.send_signal(sig)
  process.send_signal(sig)
#

if __name__ == '__main__':

  if config.cfgAlertsNotifications == 1:
    # AlertsNotifications = multiprocessing.Process(target = TestNotifications)
    AlertsNotifications = multiprocessing.Process(target = AlertsNotifications)
    AlertsNotifications.start()

while True:
  try:
    bot.polling(none_stop=True, timeout=10) #constantly get messages from Telegram
  except:
    bot.stop_polling()
    time.sleep(5)
  finally:
    kill()
