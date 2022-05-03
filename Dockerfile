FROM python:3.10.2

# FRONT
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated vim nginx supervisor git

# BACK
RUN pip3 install uvicorn fastapi xmltodict pymysql pandas requests Jinja2
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

COPY ./config/server.conf /etc/nginx/conf.d/server.conf
COPY ./config/programs.conf /etc/supervisor/conf.d/programs.conf

COPY ./ /app
WORKDIR /app/front
RUN npm install
RUN npm run build
WORKDIR /app

ENTRYPOINT ["supervisord", "-n"]
