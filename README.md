# Django 2.0+ API project template

This this a fork extending @jpadilla's Django template. It integrates the [Django Rest Framework](https://www.django-rest-framework.org/) and [celery](https://celeryproject.org).

This boilerplate is not suited for smaller projects and required tweaking. It includes a minimal boilerplate to get you started.
## Features

- Django 2.0+
- Django Rest Framework out-of-the-box
- Ready-to-deploy docker-compose configuration
- Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
- Development, Staging and Production settings with [django-configurations](https://django-configurations.readthedocs.org).
- Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
- Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
- HTTPS and other security related settings on Staging and Production.
- PostgreSQL database support with psycopg2.

## How to install

```bash
$ django-admin startproject --template https://github.com/fronbasal/django-project-template/archive/master.zip --extension=py,md,env,yml,ini,sh project_name
$ mv example.env .env
$ pipenv install --dev
```

## Environment variables

These are common between environments. The `ENVIRONMENT` variable loads the correct settings, possible values are: `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT="DEVELOPMENT"
DJANGO_SECRET_KEY="dont-tell-eve"
DJANGO_DEBUG="yes"
```

These settings(and their default values) are only used on staging and production environments.

```
DJANGO_SESSION_COOKIE_SECURE="yes"
DJANGO_SECURE_BROWSER_XSS_FILTER="yes"
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF="yes"
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS="yes"
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_REDIRECT_EXEMPT=""
DJANGO_SECURE_SSL_HOST=""
DJANGO_SECURE_SSL_REDIRECT="yes"
DJANGO_SECURE_PROXY_SSL_HEADER="HTTP_X_FORWARDED_PROTO,https"
```

## Deployment

This project template includes Docker deployment files.

## License

The MIT License (MIT)

Copyright (c) 2012-2017 José Padilla

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
