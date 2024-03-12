# Поиск вакансий по программированию в России


## Обзор 

Этот проект содержит скрипты для анализа и сравнения зарплат по вакансиям программирования в России, используя данные с сайтов _SuperJob_ и _HeadHunter_. Скрипты используют API для получения списка вакансий по различным языкам программирования и рассчитывают среднюю зарплату для каждого языка на основе предложенных диапазонов зарплат. Результаты отображаются в таблицах ASCII, обеспечивая четкую и доступную статистику зарплат.

## Как использовать

__Клонировать репозиторий:__

```python
git clone https://github.com/Rokyl59/search_vacancies.git
```

__Установите зависимости:__

Убедитесь, что в вашей системе установлен Python 3. Используйте `pip` (или `pip3`) для установки необходимых зависимостей:

```python
pip install -r requirements.txt
```

__Получение токена SuperJob:__

Чтобы использовать скрипт, вам понадобится персональный токен _SuperJob_. Чтобы его получить:

* Зарегистрируйтесь на сайте [SuperJob](https://api.superjob.ru/) и получите токен.

__Настройка окружения:__

Создайте файл `.env` в корневом каталоге скрипта и добавьте в него следующую строку:

```
SJ_API_KEY=ВашSuperJobApiKey
```

* Замените `ВашSuperJobApiKey` на ваш фактический токен SuperJob.

## Использование

__Загрузка и хранение изображений:__

* Получение и анализ данных о вакансиях:

```python
python main.py
```

## Примечания

* Проверьте, что ваш файл .env правильно настроен с вашим ключом API SuperJob, чтобы избежать ошибок неавторизации.

* Скрипты автоматически создают ASCII таблицы, отображающие количество найденных вакансий, количество обработанных вакансий и среднюю зарплату для каждого языка программирования.

* Вы можете добавить или удалить языки программирования из списка languages в скрипте, чтобы настроить анализ.

* Для получения данных с API требуется интернет-соединение.

* Обращайтесь с вашими ключами API безопасно и не делитесь ими публично.
 
