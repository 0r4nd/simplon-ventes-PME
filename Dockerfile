FROM python:3.8.6-buster

# création utilisateur 'user' ainsi que son répertoire
# puis on spécifie le workdir
#RUN useradd -ms /bin /bash user
#USER user
#WORKDIR /home/user

# copie de tous les fichiers et dossiers utiles vers le docker
COPY app /app
COPY data /data
COPY requirements.txt requirements.txt

# update de pip puis installation de toutes les librairies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# execute le code depuis le container
CMD uvicorn app.main:app --host 0.0.0.0
