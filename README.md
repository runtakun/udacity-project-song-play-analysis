# Song Play Analysis (Udacity Lesson 1)

## Description of this project
Load song play data of a mobile application and register to PostgreSQL database.

## ETL process
ETL consists from two processes; load song data and log data.

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
