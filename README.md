# Technische Dokumentation

## Local commands

- create migration after model change:
`python3 manage.py makemigrations`
- migrate to current version:
`python3 manage.py migrate`
- dump current database into fixture file (override fixture file):
`python3 manage.py dumpdata > fixture.json`
- load test data:
`python3 manage.py loaddata fixture.json`
- create superuser (to access staff page)
`python3 manage.py createsuperuser`


## Docker
### First start
- Build images and run containers
`docker-compose -f docker-compose.dev.yml up --build`
- Start previously built containers in background
`docker-compose start`
- Apply migrations
`docker exec backend python3 manage.py migrate`
- Collect static files
`docker exec backend python3 manage.py collectstatic`
- Load test data:
`docker exec backend python3 manage.py loaddata fixture.json`

### Development
File changes in python files trigger an auto-reload of the server.
Migrations have to be executed with `docker exec backend python3 /matchedmedisvirus-backend/manage.py migrate`.

After changes to the Docker configuration, you have to restart and build the containers with `docker-compose -f docker-compose.dev.yml up --build`.

## Translation
- Add translatable strings in python with `_("Welcome to my site.")` and import `from django.utils.translation import gettext as _` ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-python-code))
- Add translatable strings in templates with `{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}` or alternatively with the `trans` block and include `{% load i18n %}` at the top ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-template-code))
- Update the translation file
`django-admin makemessages -l en --no-location`
- Edit translations in `backend/locale/en/LC_MESSAGES/django.po`

## Production
Set `SECRET_KEY` and `SENDGRID_API_KEY` in `backend.prod.env` for Django 
`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`  inside `database.prod.env` for postgres on your host machine.
Also add a `SLACK_LOG_WEBHOOK` to enable slack logging.

To run a container in production and in a new environment execute the `setup.sh` script which builds the containers, runs all configurations and starts the web service.

If you want to deploy manually follow these steps closly:

1. Build the containers
2. Make messages
3. Compile messages
4. Collect static
5. Migrate
6. Restart the backend container (important, whitenoise does not reload static files after it has started)

## Testing

For executing the tests use `python3 manage.py test`. 

In case you add more required environment variables for productions, please check for their existance in `backend/apps/checks.py`.

## Logging

Logging should always use the following pattern if possible:

```
import logging
logger = logging.getLogger(__name__)
logger.info('message',extra={ 'request': request })
```

If the request is not logged as an extra parameter, the log entry will **NOT** be messaged to slack!

Adding the request as extra parameter will automatically extract logged on user information as well as POST variables and take care of removing sensitive information from
the logs, respecting the @method_decorator(sensitive_post_parameters()). For example in user sign in, this will prevent logging of passwords.

**Warning:** Special care must be taken to avoid errors from circular references. The extra parameters are written to the log file and serialized as JSON. Circular references will cause
logging failure. One example would be adding the student to the extra dict:

Student has an attribute for the user, user has an attribute for the student, ... 

These circular references will prevent the log entry from being written. 
Including request is always safe, because the logging formatter contains dedicated code for request logging.

## Javascript

This project uses webpack to create javascript bundles. Custom Javascript is only added to pages when it is needed to enhance default Django functionality or to create user experience improvements.

Notable examples are
- Map Views
- User Profile to hide unneeded blocks

Javascript sources are created in frontend/src folder

To build them node needs to be installed. We suggest using [Node Version Manager](https://github.com/nvm-sh/nvm) to install node. Dependencies can be installed using 

```
cd frontend && npm install
```

### Build 

All commands need to be executed in `./frontend`

- Build javascript bundles
`npm run build`
- Build javascript bundles in devMode and rebuilt when changes are made
`npm run dev`

### Loading bundles

To load a bundle in a django template add the following tags:
```
{% load render_bundle from webpack_loader %}
{% render_bundle 'student' %}
```

Django will then use the webpack-stats.json to determine which file from dist folder to include.
The dist folder has been added to the STATICFILES_DIRS so it will be found automatically

### Adding new bundles

When creating new bundles add an entry in `webpack.config.js` under `entry`:
```
  entry: {
    main: ['./src/main.js'],
    ....
    new_bundle: ['./src/new_bundle.js'],
  },
```

As a rule of thumb, new bundles should be created in the src directory, their modules should be loaded from the sub-directories. A page should only ever load one bundle. If modules are needed in several bundles, just require them

#### JQuery

JQuery is loaded as a part of the bootstrap initialization. This will be kept in the main django project codebase.
It is not necessary to load jQuery via webpack, an external reference can be used. (See [https://webpack.js.org/configuration/externals/](https://webpack.js.org/configuration/externals/))