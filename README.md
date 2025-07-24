## Клонирование репозитория и запуск приложения
```
git clone https://github.com/xaslx/tron.git
cd tron
```

```
poetry install
poetry shell
```


```
make app	Запускает приложение
make app-down	Останавливает и удаляет контейнеры
make app-logs	Просмотр логов приложения fastapi
make alembic-revision	Создаёт новую миграцию
make alembic-upgrade	Применяет миграции к базе данных
```
