#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ##### Observer Config
# Edit starts here

TgBotAPIKey = '' # API Keythat you get from @BotFather
tg = [] # Your id, you can get it by sending command /userid to bot

mainSite = "https://ethereum.oxen.io"

# Observer will check that this string is in the title of the webpage, if the website does not return this string it will be considered down
titleString  = "wOxen Bridge"

#this is an example get request to call to the backend, will check if the result of this get request is 200
apiRequest = ""

# Address to monitor token and eth
hotWalletAddress = ''

# Threshold in full token Units (Not Atomic)
lowBalanceThreshold = 100000

# Threshold in full Ethereum Units (Not Atomic)
lowEthThreshold = 1

# Contract that defines token and its details
contractAddress = '0xd1e2d5085b39b80c9948aeb1b9aa83af6756bcc5'
decimals = 9

# Infura endpoint to call
ethereumHTTPProvider = 'https://mainnet.infura.io/v3/xxxxxxxxxxxxxxx'

# Edit ends here

# Other

#Enables or disables alerts (1 for on, 0 for off)
cfgAlertsNotifications = 1

# ##### /Observer Config
