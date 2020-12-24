FROM python:3.8

EXPOSE 80:80

RUN python -m pip install --upgrade pip

RUN pip install pipenv

RUN mkdir -p /application/

COPY Pipfile Pipfile.lock /application/

WORKDIR /application/

RUN pipenv install --deploy --system --ignore-pipfile

WORKDIR /application/dealsmaster/

CMD gunicorn dealsmaster.wsgi --bind 0.0.0.0:80