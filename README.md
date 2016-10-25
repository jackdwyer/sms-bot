# sms-bot

> Takes sms as input, dumps message into google spreadsheets


## Setup host
`make setup-docker-host`

## Update host scheduling
`make setup-docker-host`

## deploy latest build
`make deploy-latest`

### notes
look at the environment variable SPREADSHEET_CONFIG to see how the sheet is setup

## TODOs
[0] have msg == 't' return next 2 trains leave from [http://mta_ui.thundercloud.club](http://mta_ui.thundercloud.club)

## DONE
[*] name the containers so that I can look up container_id and grab the logs
