# pull official base image
FROM python:3.8

# create directory
RUN mkdir -p /home/www/scraper
# RUN mkdir -p /home/www/scraper/media

# set work directory
WORKDIR /home/www/scraper

# copy project
COPY . /home/www/scraper

# install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get -y update
#RUN apt-get -y upgrade
#RUN apt-get install -y sqlite3 libsqlite3-dev
#RUN mkdir /db
RUN chmod a+x ./entrypoint.sh

# EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH
# ENTRYPOINT ["entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "core.wsgi", "--reload"]