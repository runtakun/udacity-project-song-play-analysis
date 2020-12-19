# Song Play Analysis (Udacity Data Engineering Nanodegree Project `Data Modeling with Postgres`)

## Description of this project
Load song play data of a mobile application and register to PostgreSQL database.

## ETL process
ETL consists from two processes.

- load song and user's song play data.
- save them to database

## How to set up

```shell
# pull docker images (if not exists on local machine) and run necessary process
docker-compose up --build -d
# if you use jupyter notebook, run following command to activate sql extension
docker-compose exec notebook pip install -r requirements.txt
# create tables
docker-compose exec app python3 create_tables.py
# run ETL
docker-compose exec app python3 etl.py
```

# ERD

![image](https://github.com/runtakun/udacity-project-song-play-analysis/blob/main/erd.png)
