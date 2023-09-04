Deployment:

#### Запуск в docker
1. Run from root directory:
    ```bash
    docker-compose up -d
    ```
On first launch:
1. Make migrations:
    ```bash
    docker-compose exec web python manage.py makemigrations && docker-compose exec web python manage.py migrate
    ```
2. Load default roles into db:
    ```bash
    docker-compose exec web python manage.py loaddata roles
    ```