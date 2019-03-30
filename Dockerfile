FROM python:3.7-slim

RUN useradd flask

WORKDIR /home/flask

# COPY requirements.txt requirements.txt
# COPY gunicorn_config.py gunicorn_config.py
# RUN python -m venv venv
# RUN venv/bin/pip install -r requirements.txt
# RUN venv/bin/pip install gunicorn

RUN pip install Flask matplotlib scipy pandas requests beautifulsoup4 lxml
RUN pip install gunicorn
COPY meteogram meteogram
COPY gunicorn_config.py gunicorn_config.py
COPY flask_server.py flask_server.py


# RUN chown -R flask:flask ./
# USER flask

EXPOSE 5000
#ENTRYPOINT ["python", "flask_server.py"]
ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "flask_server:app"]
