# kaizen
[![Docker Image CI](https://github.com/saladware/kaizen/actions/workflows/docker-image.yml/badge.svg)](https://github.com/saladware/kaizen/actions/workflows/docker-image.yml)

**kaizen** - _система управления предложениями по улучшению_

![Kaizen.png](./docs/Kaizen.png)

## Техническое задание
Техническое задание проекта системы можно посмотреть [здесь](./docs/technical_requirements.md)

## Запуск

Для запуска системы необходимо [установить docker-compose](https://docs.docker.com/get-docker/)
```commandline
docker-compose up -d
```
При первом запуске системы, необходимо запустить миграции для создания таблиц базы данных
```commandline
docker-compose exec app alembic upgrade head
```
