# Автоновости Ukr.net

Рассылка автоновостей с сайта ukr.net

# Настройка

Для настройки используйте файл config.json

```json
{
  "main_link": "https://www.ukr.net/news/dat/avto/", # Ссылка на сайт
  "last": 10, # Сколько последних новостей проверять
  "sleep": 60, # Задержка между проверками, секунды
  "retry sleep": 120, # Задержка после ошибок, секунды
  "max description len": 512, # Максимальная длина описания (больше 1024 символов нельзя)
  "post without image": 0, # Публиковать если нет без изображения
  "post without description": 0, # Публиковать если нет описания
  "log file": 1, # Выводить ли логи в файл exception.logs
  "headers": { # Заголовки запроса
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
    "connection": "keep-alive"
  }
}
```
