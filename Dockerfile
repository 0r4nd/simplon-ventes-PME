FROM python:3.10.6-slim

# dossier pour l'application
WORKDIR /app

# copie de tous les fichiers et dossiers utiles vers le docker
COPY . /app

# update de pip puis installation de toutes les librairies
RUN pip install -r requirements.txt

# execute le code depuis le container (à commenter si lancé depuis docker-compose)
CMD uvicorn app.main:app --host 0.0.0.0
