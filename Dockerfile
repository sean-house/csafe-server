FROM python:3.7
# Get the MS ODBC Drivers
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB3E94ADBE1229CF
RUN apt-get update \
        && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
        && apt-get install -y unixodbc \
        && apt-get install -y unixodbc-dev \
        && apt-get update

RUN mkdir /csafe-server
WORKDIR /csafe-server

ADD requirements.txt /csafe-server/
RUN pip install -r requirements.txt
ADD . /csafe-server/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

# Set non-secret Environment variables
ENV CSAFE_INTENT=DOCKER
RUN python manage.py collectstatic
EXPOSE 8000 2222
#CMD ["python", "/csafe-server/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["init.sh"]
