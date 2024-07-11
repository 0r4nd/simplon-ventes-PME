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
  docker build -t app .
```

Run docker image:
```sh
  docker run -p 8000:8000 app
```

Run docker image (interactively)
```sh
  docker run -it app sh
```
<br>

## docker-compose

Build
```sh
docker-compose up -d
```
```sh
docker-compose -f docker-compose.yml up -d
```

état des services
```sh
docker-compose ps
```
<br>
