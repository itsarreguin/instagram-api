# Instagram API

Simple Instagram API clone built on Django.

---

## Start up the project

The next steps are assistance to start using the instagram API clone.

---

### Clone project repo

Clone the project using one of the next commands (using https or ssh).

```shell
git clone https://github.com/itsarreguin/instagram-api.git
```

```shell
git clone git@github.com:itsarreguin/instagram-api.git
```

---

### Create a virtual env

To create the Python virtual environment we will use the default python venv module.

```shell
python -m venv <virtualenv_name>
```

#### Virtualenv activation and deactivation

Activation on MacOS and Linux.

```shell
python source <virtualenv_name>/bin/activate
```

Activation on Windows using Powershell

```shell
python .\<vitualenv_name>\Scripts\activate
```

#### Deactivation

To deactivate your virtualenv only use the next command, this works on the three operating systems.

```shell
deactivate
```

---

### Installing dependencies

The project has the requirements folder and requirements.txt file, this last is just an extension of dev.txt file inside the requirements folder.

```shell
pip install -r requirements.txt
```

---

### Running the API

Once the dependencies are installed you can start running the API

```shell
python manage.py runserver
```

If the Django's default port is occupied on your computer change this in the same command

```shell
python manage.py runserver <port>

python manage.py runserver 8080
```

#### Create your superuser

If you wanna create an admin superuser run the next command and fill in all fields

```shell
python manage.py createsuperuser
```

### Celery and RabbitMQ

The Instagram API project uses Celery and RabbitMQ to run background tasks, execute in new shell's the next commands

#### Running Celery

```shell
celery -A instagram.tasks:celery worker --loglevel=info -P threads
```

Add the broker url in your .env file

```text
CELERY_BROKER_URL=amqp://localhost:5672
```

#### Running RabbitMQ

In my case, I use Docker to run a RabbitMQ instance using the following command

```shell
docker run --rm -it -p 5672:5672 rabbitmq
```

The previous command runs the latest version of RabbitMQ in Docker, when press Ctrl + C the container to be removed.

#### Using Redis for Celery

If you wanna use Redis to run tasks follow the next steps

- Run a Redis docker container or install redis on your computer

    ```shell
    docker run --rm -it -p 6379:6379 redis
    ```

- Add redis url in your .env file

    ```text
    CELERY_BROKER_URL=redis://localhost:6379
    ```

- Repeat the command to run Celery once again

> Note: Redis client has already been included in this project

### Dependencies links

1. Django:
    + Documentation: [djangoproject.com](https://djangoproject.com/)
    + Repository: [github.com/django/django/](https://www.github.com/django/django)

2. Django REST Framework
    + Documentation: [django-rest-framework.org](https://www.django-rest-framework.org)
    + Repository: [github.com/encode/django-rest-framework](https://www.github.com/encode/django-rest-framework/)

3. Celery:
    + Documentation: [docs.celeryq.dev](https://docs.celeryq.dev/)
    + Repository: [github.com/celery/celery](https://www.github.com/celery/celery/)

4. PyJWT
    + Repositroy: [github.com/jpadilla/pyjwt](https://github.com/jpadilla/pyjwt)

### Credits

Made with <3 and code by <[@itsarreguin](https://twitter.com/itsarreguin/)>

Instagram is a Meta, Inc. trademark.
