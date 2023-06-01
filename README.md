# REST сервис - Дни рождения

### Как пользоваться сервисом:
Перейдите по адресу:

        ...

Что бы делать запросы зайдите в:

        ...

Что бы авторизоваться на моей ВМ:

        login: skypro
        password: skypro

# Как я развернул проект:

## 1.
1. Создаем приложение отсылающееся из config.py 

2. Надо чекать что создание базы данных не было в if __name__ == '__main__':
with app.app_context():
    db.create_all() -> должно быть выше if __name__ == '__main__':


3. Создаем default_config.py
```python
class Config:
    """
    Создание конфигурации приложения
    """
    DEBUG = True # Включаем режим отладки (Debug mode)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db' # URI для подключения к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Отключить отслеживание изменений моделей SQLAlchemy
```


4. Создаем docker_config.py
```python
class Config:
    """
    Создание конфигурации приложения
    """
    DEBUG = True # Включаем режим отладки (Debug mode)
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_app:flask_app_password@pg/flask_app' # URI для подключения к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Отключить отслеживание изменений моделей SQLAlchemy
```

5. Проверяем что все запросы работают


## 2.
6. Создаём Dockerfile

```Dockerfile
FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80
```
Примечание при создании REST и наличии функции create_app, в if __name__ == '__main__' в app.py нужно следующее:
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
A в Dockerfile должно быть CMD python app.py

7. Создаем docker-compose.yaml
```yaml
version: "3.9"

services:
  api:
    build:
      context: .
    ports:
      - 80:80
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:
      pg:
        condition: service_healthy
  pg:
    image: postgres:latest
    environment:
      POSTGRES_USER: flask_app
      POSTGRES_PASSWORD: flask_app_password
      POSTGRES_DB: flask_app
    volumes:
      - ./pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```
### Что тут делаем?

        1) image не нужен, зато нужен build
    
        2) Проверяем связь environment и docker_config.py

8. Создаём requirements.txt - через терминал
        
        pip install psycopg2-binary 
        pip3 freeze > requirements.txt


9. Удаляем все образы на всякий случай

        docker rm -f <ID>
        docker system prune
        docker system prune -a

10. Поднимем docker-compose и проверим что он собирается 

         docker-compose up --build -d


11. Проверяем что всё работает

         [+] Running 3/3
         ⠿ Network notesproject_default  Created                                                                                                                          0.0s
         ⠿ Container notesproject-pg-1   Healthy                                                                                                                         11.7s
         ⠿ Container notesproject-api-1  Started   

12. Проверяем логи docker-compose

        docker-compose logs
Еcли нет критических ошибок (role "postgres" does not exist - не важен), то всё работает.

13. Смотрим что методы и всё остальное работает на localhost

## 3.

14. Создаём docker-compose-ci.yaml

        Добавляем image и туда пишем репозиторий из Docker Hub который нужно создать, по типу: image: dockerusername/repository:tag

```yaml
version: "3.9"

services:
  api:
    image: thefimerhub/exam_rep:$GITHUB_REF_NAME-$GITHUB_RUN_ID
    ports:
      - 80:80
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:
      pg:
        condition: service_healthy
  pg:
    image: postgres:latest
    environment:
      POSTGRES_USER: $DB_USER
      POSTGRES_PASSWORD: $DB_PASSWORD
      POSTGRES_DB: $DB_NAME
    volumes:
      - ./pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

15. Создаем docker_config_ci.py
```python
class Config:
    """
    Создание конфигурации приложения
    """
    DEBUG = True # Включаем режим отладки (Debug mode)
    SQLALCHEMY_DATABASE_URI = "postgresql://$DB_USER:$DB_PASSWORD@pg/$DB_NAME" # URI для подключения к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Отключить отслеживание изменений моделей SQLAlchemy
```

16. Создаём 2 папки в корне проекта .github/workflows и в workflows создаём action.yaml
Вот пример файла:
```yaml
name: Build and deploy workflow
on: [push]
jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: clone code
        uses: actions/checkout@v2
      - name: docker build
        run: docker build -t thefimerhub/docker_hub_repository:$GITHUB_REF_NAME-$GITHUB_RUN_ID .
      - name: docker login
        run: echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
      - name: docker push
        run: docker push thefimerhub/docker_hub_repository:$GITHUB_REF_NAME-$GITHUB_RUN_ID
  deploy:
    runs-on: ubuntu-latest
    needs: build_and_push
    env:
      DB_USER: ${{ secrets.DB_USER }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
      DB_NAME: ${{ secrets.DB_NAME }}
    steps:
      - name: clone code
        uses: actions/checkout@v3
      - name: render configs
        run: |
          mkdir deploy
          cat docker-compose-ci.yaml | envsubst > deploy/docker-compose.yaml
          cat docker_ci_config.py | envsubst > deploy/docker_config.py
      - name: copy files to server
        uses: appleboy/scp-action@v0.1.4
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
          source: "deploy/docker-compose.yaml,deploy/docker_config.py"
          target: "rename"
          strip_components: 1
      - name: deploy app
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
          script: |
            cd rename
            echo ${{ secrets.PASSWORD }} | sudo -S docker-compose up -d
```


17. Загружаем репозиторий на гитхаб с задокенным action.yaml. И делаем секреты для:

        DOCKER_TOKEN - создаем в настройка Docker Hub
        DOCKER_USERNAME - имя пользователя в Docker Hub
        HOST - из Yandex Cloud (IPv4)
        USERNAME - имя пользователя на ВМ
        PASSWORD - пароль от пользователя на ВМ
        DB_USER - имя полльзователя БД
        DB_PASSWORD - пароль от БД
        DB_NAME - название БД

18. Убираем все ненужные и запущенные прошлые образы на ВМ

19. Пушим репозиторий на гитхаб и раздоким action.yaml
        
        