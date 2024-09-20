# insurance-app

### Set up
1. `docker-compose up --build -d` to launch containers in the root
2. `docker-compose exec api alembic upgrade head` to run the migrations

### Documentation of the api
visit `http://localhost:8000/docs` to test the GET /health and GET /policies/{policy_id}