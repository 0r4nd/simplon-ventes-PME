FROM python:3.8.6-buster

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY simplon_vente_pme /simplon_vente_pme
COPY datasets /datasets

RUN pip install --upgrade pip
