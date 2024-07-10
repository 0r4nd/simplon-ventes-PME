# Utils

## Uvicorn
Launch api with uvicorn:
```sh
  uvicorn app.main:app --reload
```
<br>

## docker
Build docker image:
```sh
  docker build -t api .
```

Run docker image:
```sh
  docker run -p 8000:8000 api
```

Run docker image (interactively)
```sh
  docker run -it api sh
```
<br>

## docker-compose

Build
```sh
docker-compose up --build
```
<br>
