# Bridge Observer

Monitors a website frontend and backend and also watches a contract and ensures its Eth Balance and Token Balance is sufficient.

Designed to monitor the wOxen Bridge (ethereum.oxen.io) and warn via telegram if the website is down or if the wOxen balance on the hotwallet dropped below a threshold.

UserIDs from telegram are added to config.tg [xxxx,yyyy] and will message all users in this config. You can identify your id by calling `/userid` on the bot

## Get Started

Run using docker
`docker build -t observerimage .`
`docker run -d observerimage`

Kill a running docker image. Find the docker process and call kill
`docker ps`
`docker kill xxxxxxx`

Or for a one liner if observerimage is image name
`docker kill $(docker ps -q --filter ancestor=observerimage)`

## Using Makefile

`make build`
`make run`
`make stop`
