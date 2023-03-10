# Техническое задание системы "Кайдзен"

## 1. Введение

Цель проекта - разработать систему управления предложениями по улучшению.
Потенциальные клиенты - организации, использующие модель внедрения предложений по улучшению для достижения повышения
результативности производства.

## 2. Описание системы

Система состоит из следующих функциональных блоков:

+ Функционал пользователя
+ Функционал автора предложения
+ Функционал контроллёра
+ Функционал участника и председателя комисси по ППУ
+ Панель администратора

### 2.1 Типы пользователей

Система предусматривает 5 типов пользователей:

+ Сотрудник
+ Контролёр
+ Член комиссии по ППУ
+ Председатель комиссии по ППУ
+ Администратор

В соответсвии с типом пользователя, у него появляются определённые функциональные возможности и определённый уровень
доступа к системе.
Сотрудник - базавый тип пользователя в системе. Предусматривается присвоение этого типа пользователя сотружникам
организации, не заведующим жизненным циклом ППУ.
Последующие типы пользователей так или иначе имеют существенную роль в обработке и реализации ППУ.
Пользователь с ролью Администратор обладает неограниченым доступом к системе. Предусматривается присвоение этого типа
пользователя только доверенному лицу, которое имеет специализацию в области информационных технологий.

### 2.2 Регистрация пользователя

Регистрация пользователя в системе осуществляется Администртором через панель администратора. Предусматривается, что по
необходимости интеграции польхователя в систему,
администратор зарегестрирует его как пользователя в системе, после чего сотруднику будут предоставлены данные для входа
в систему (логин, пароль).

При регистрации пользователя, Администратор уквазывает следующий набор данных:

+ ФИО сотрудника
+ Электронная почта сотрудника
+ Отдел сотрудника
+ Должность сотрудника
+ Пароль

### 2.3 Coming soon

## 3. Требования к безопасности

+ HTTP запросы к API сервиса должны шифроваться, согласно стардарту HTTPS при помощи верифицированного SSL сертификата
+ Исходный код компонентов системы не должен содержать конфеденциальные данные: секретные ключи, пароли, токены и т. п.
+ Система должна быть устойчева к таким видам хакерских атак, как SQL Injection, CSRF attack, DoS, DDoS, XXS и другим.

## 4. Требования к дизайну

Дизайн графического интерфейса сервиса должен быть выполнен в минималистичном стиле. Акцент на контент. Должна быть
возможность для изменения цветового акцента темы и логотипа сервиса согласно требованиям клиента. 

## 5. Используемые технологии

Для разрабокти сервиса используется следующий набор технологий:
+ Бекенд
  - Python 3 - язык программирования
  - uvicorn - WSGI-сервер
  - FastAPI - веб-фреймворк
  - PostgreSQL - база данных
  - SQLAlchemy - ORM
  - alembic - инструмент для создания миграций
+ Фронтенд
    - TypeScript - язык программирования
    - React - веб-фреймворк

Используемый набор технологий может изменяться по необходимости Исполнителя в свободном порядке.