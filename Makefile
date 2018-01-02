.PHONY: help

status:
		docker-compose ps

stop:
		docker stop $(shell docker ps -aq)

clean:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)

destroy:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)
		docker rmi -f $(shell docker images -q)

run:
		docker-compose -f docker-compose.yml up --build -d
		docker exec -it $(shell docker ps -q --filter "name=users_service_1") go run db/dbmigrate.go
		docker exec -it $(shell docker ps -q --filter "name=famous_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=politics_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=sports_news_service_1") python dbmigrate.py

run-test:
		docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build -d
		docker exec -it $(shell docker ps -q --filter "name=users_service_1") go run db/dbmigrate.go
		docker exec -it $(shell docker ps -q --filter "name=famous_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=politics_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=sports_news_service_1") python dbmigrate.py
		go run ${PWD}/TestRobot/main.go
		docker exec -it $(shell docker ps -q --filter "name=orcherstrator_news_service_1") python tests.py
		docker exec -it $(shell docker ps -q --filter "name=orcherstrator_news_service_1") python tests_integration.py

migrate:
		docker exec -it $(shell docker ps -q --filter "name=users_service_1") go run db/dbmigrate.go
		docker exec -it $(shell docker ps -q --filter "name=famous_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=politics_news_service_1") python dbmigrate.py
		docker exec -it $(shell docker ps -q --filter "name=sports_news_service_1") python dbmigrate.py
