FROM alpine
# Forked from https://github.com/jazzdd86/alpine-flask
# Edited by Sam van Herwaarden <samvherwaarden@gmail.com>

# basic flask environment
RUN apk add --no-cache bash git nginx uwsgi uwsgi-python3 \
                       g++ python3-dev libffi-dev \
	&& pip3 install --upgrade pip \
	&& pip3 install flask Flask-Login Flask-Mail Flask-SQLAlchemy \
	&& pip3 install Flask-Principal Flask-WTF \
	&& pip3 install passlib bcrypt itsdangerous \
	&& pip3 install git+https://github.com/mattupstate/flask-security.git@develop \
	&& pip3 install hyper googletrans 

# local directory structure
ENV APP_DIR /app
ENV DATA_DIR /data

RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& mkdir ${DATA_DIR} \
	&& chown -R nginx:nginx ${DATA_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R

VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}

VOLUME ${DATA_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini
COPY entrypoint.sh /entrypoint.sh

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
