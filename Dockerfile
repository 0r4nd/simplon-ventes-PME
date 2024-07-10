FROM python:3.8.6-buster

# dossier pour l'application
WORKDIR /app

# copie de tous les fichiers et dossiers utiles vers le docker
COPY app /app
COPY data /data
COPY requirements.txt ./

# update de pip puis installation de toutes les librairies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# execute le code depuis le container (à commenter si lancé depuis docker-compose)
#CMD uvicorn app.main:app --host 0.0.0.0
