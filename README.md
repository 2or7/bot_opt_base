# # Оптимизация системы управления пропусками для оптовой базы

Этот репозиторий содержит исходный код для создания Телеграм-бота, который будет автоматически управлять выдачей пропусков и предоставлять информацию для водителей и арендаторов оптовой базы.

## Описание проекта

В оптовой базе существует необходимость в эффективной системе управления пропусками для автомобилей. Существующий процесс предполагает отправку заявок и выдачу пропусков операторами в Бюро Пропусков. Этот процесс можно существенно оптимизировать с помощью Телеграм-бота.

## Основные функции Телеграм-бота

### Для водителей:
- Поиск пропуска и ключа для получения в Бюро Пропусков.
- Просмотр информации о текущей ситуации на территории базы:
  - Количество автомобилей на территории.
  - Количество свободных мест для заезда.

### Для арендаторов:
- Просмотр общей информации о текущей ситуации:
  - Количество заявок.
  - Количество выданных пропусков.
  - Количество автомобилей на территории.
  - Количество свободных мест для заезда.
  - Количество завершенных заявок.
- Поиск детальных данных по конкретному автомобилю:
  - Проверка наличия пропуска.
  - Информация о времени заезда и выезда.

## Использование

Для начала использования бота, вам необходимо создать бота в Telegram и получить токен API. Затем установите необходимые зависимости, указанные в файле `requirements.txt`. После этого, вы можете запустить бота с помощью команды:

```bash
python main.py
```

Бот будет доступен в Telegram, и пользователи могут начать взаимодействие с ним, следуя предоставленным командам.

## Демонстрация работы
Для наглядности, здесь предоставлена ссылка на видео, демонстрирующее функциональность киоска для поиска пропусков: [ссылка на видео](вставьте ссылку на видео).

## Развитие проекта
Этот проект может быть доработан и расширен следующими способами:

- Добавление возможности регистрации и аутентификации пользователей.
- Интеграция с базой данных для хранения информации о пропусках и заявках.
- Расширение функциональности бота для обработки заявок и автоматической генерации пропусков.
- Создание веб-панели администратора для управления системой.