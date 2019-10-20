# Market API
Market API Rest

## Getting Started
Following these instructions will make this project running in your local machine development.

### Prerequisites
```buildoutcfg
- Python
- Docker
- Postgres
```

### Installing

```buildoutcfg

1- git clone
2- cd market
2.1- docker-compose up -d (In case that you don't have docker installed, postgres can take care of the database connection)
3- python3 -m venv env
4- source env/bin/activate
5- pip install -r requirements.txt
6- python3 manage.py migrate

```

### To run
```buildoutcfg
python manage.py runserver
```


#### Note: sqllite is the database that all tests are being run

### Pagination
Actualy DRF is taking care of the pagination, however the limit for list objects are 5. To go to the next page you will found `next` or `previous` word along of the response of the api
The configuration for it can be found on `settings.py` file under the `api/magalu` folder:

`PAGE_SIZE=5`

### Running tests

```buildoutcfg
python manage.py test
```

### Running app
```buildoutcfg
python manage.py runserver
```

### Available URLS:
```buildoutcfg
http://localhost:8000/api/v1/api-token-auth/
http://localhost:8000/api/v1/product/
http://localhost:8000/api/v1/product-review/
http://localhost:8000/api/v1/user/
http://localhost:8000/api/v1/wish-list/
http://localhost:8000/api/v1/wish-list-product/
```

## Author

* **Daniel Santos** - *Trying to keep simple and clean* - [drsantos20](https://github.com/drsantos20)