all: build run

build:
	docker build -t jackdwyer/smsbot:latest -f docker/Dockerfile .

run:
	docker run --env-file env -p 5000:5000 -v $(CODE_PATH):/smsbot jackdwyer/smsbot:latest /smsbot/bot.py

console:
	docker run -it --env-file env -p 5000:5000 -v $(CODE_PATH):/smsbot jackdwyer/smsbot:latest /bin/sh

deploy-latest: build
	docker push jackdwyer/smsbot:latest
	ssh root@$(HOST) /root/cycle_container.sh

clean-id-file:
	ssh root@$(HOST) rm /tmp/smsbot.id

setup-docker-host:
	scp env root@$(HOST):/root/sms-bot-env
	scp cycle_container.sh root@$(HOST):/root/

ssh-host:	
	ssh root@$(HOST)
