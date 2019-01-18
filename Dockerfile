FROM python:3.6.8

LABEL Name=districtr-api Version=0.0.1
EXPOSE 5000

# This is where we'll put the app:
WORKDIR /app

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from Pipfile
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --ignore-pipfile

# Copy the app into the container
COPY . /app
ENV FLASK_APP api

# Run gunicorn server in the pipenv environment:
CMD ["pipenv", "run", "gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "api:create_app()"]
