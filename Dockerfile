FROM python:3.10

RUN mkdir /shop_app

WORKDIR /shop_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker_scripts/*.sh