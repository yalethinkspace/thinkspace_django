# Thinkspaces

## Local development

1. Setup a virtual environment

    ```bash
    python3 -m venv ~/.virtualenvs/thinkspace
    source ~/.virtualenvs/thinkspace/bin/activate
    ```

2. Download project and install dependencies

    ```bash
    git clone https://github.com/yalethinkspace/thinkspace_django
    cd thinkspace_django
    pip3 install -r requirements.txt
    ```

3. Copy `.env.example` to `.env` and edit credentials

    ```bash
    cp .env.example .env
    nano .env
    ```

    Replace `SECRET_KEY` with any sufficiently complex string. You can generate one in Python3 using:

    ```python
    import secrets
    secrets.token_urlsafe(24)
    ```

    `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` can be obtained from the project owner (or you may provide credentials to your own SMTP server. This will also require modifying `settings.py`).

4. Start development server for testing

    ```bash
    django r
    ```

    OR

    ```bash
    python manage.py runserver
    ```

## Remote development

Points of note: 

1. Pull requests trigger Heroku review apps to be built. Find out more here: [https://devcenter.heroku.com/articles/github-integration-review-apps](https://devcenter.heroku.com/articles/github-integration-review-apps)

    You may use these review apps to debug code behavior. You may need to be added as a collaborator on the Heroku deploy by the project owner in order to fully explore this functionality.

2. `.env` credentials are already present on Heroku. For instance, email credentials are pre-configured.

