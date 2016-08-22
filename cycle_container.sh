#!/bin/bash

docker pull jackdwyer/smsbot:latest

if [[ -f /tmp/smsbot.id ]]; then
  docker kill $(cat /tmp/smsbot.id)
  rm /tmp/smsbot.id
fi

docker run -d --env-file sms-bot-env -p 5050:5000 jackdwyer/smsbot:latest /smsbot/bot.py > /tmp/smsbot.id
