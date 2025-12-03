# Project README

## Overview

This project is a Django-based Student Management System that includes features such as enrollment tracking, course management, and automated enrollment status updates using Celery and Redis.

## Features

* Student Management
* Course Management
* Enrollment System
* Automatic Monthly Enrollment Locking
* Celery Task Processing
* Docker-based Development Environment

## Technologies Used

* Python / Django
* Celery
* Redis
* Docker & Docker Compose
* PostgreSQL (optional)

## Project Structure

```
project_root/
├── yourproject/
│   ├── settings.py
│   ├── celery.py
│   ├── __init__.py
│   └── urls.py
├── enrollment/
│   ├── models.py
│   ├── tasks.py
│   └── cron.py
├── course/
├── user/
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Celery Setup

Celery is configured in `yourproject/celery.py` and automatically discovered tasks from installed apps.

### Starting Celery (Docker)

Celery runs inside Docker using the `docker-compose.yml` file. The services include:

* `django`
* `celery`
* `celery-beat`
* `redis`

Start the environment:

```bash
docker-compose up --build
```

## Automatic Monthly Enrollment Locking

Celery Beat runs a cron-like schedule and calls:

```python
enrollment.tasks.lock_monthly_enrollments
```

Which updates all enrollments to `LOCKED` at the beginning of each month.

## Docker Setup

### Build & Run

```bash
docker-compose up --build
```

### Stopping Containers

```bash
docker-compose down
```

## Environment Variables

This project uses Redis as the Celery broker. Example configuration in `settings.py`:

```python
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/1"
```

## Running Django Commands

Inside Docker:

```bash
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
```

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
