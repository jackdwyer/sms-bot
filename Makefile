all: build run

build:
	docker build -t jackdwyer/smsbot:latest -f docker/Dockerfile .

run:
	docker run --env-file env -p 5000:5000 -v $(CODE_PATH):/smsbot jackdwyer/smsbot:latest /smsbot/bot.py

# console:
#  	docker run -it --env-file env -p 5000:5000 -v $(CODE_PATH):/smsbot jackdwyer/smsbot:latest /bin/sh

update-config: setup-docker-host cycle

deploy: build deploy-latest update-config

cycle:
	ssh root@$(HOST) /root/cycle_container.sh
	
deploy-latest: build
	docker push jackdwyer/smsbot:latest

clean-id-file:
	ssh root@$(HOST) rm /tmp/smsbot.id

setup-docker-host:
	scp env root@$(HOST):/root/sms-bot-env
	scp cycle_container.sh root@$(HOST):/root/

console:
	ssh root@$(HOST)

prod-logs:
	ssh root@$(HOST) docker logs -f a94c43670393
