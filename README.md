# insurance-app

This web application uses Python FastAPI for RESTful APIs, with a PostgreSQL database, deployed to AWS via ECS on EC2s. The endpoint supplied in the email can be used to access the deployed application.

Locally the project can be run using docker.

### Set up
1. `docker-compose up --build -d` to launch containers in the root
2. `docker-compose exec api alembic upgrade head` to run the migrations

The database is seeded and so the GET /policies/{policy_id} endpoint can be hit with postman locally at e.g. `http://localhost:8000/policies/1`

### Documentation of the api
visit `http://localhost:8000/docs` to test the GET /health and GET /policies/{policy_id} locally in the browser

### Infrastructure setup
1. Given existing aws account and aws cli installed locally, create a new private registry in AWS ECR named 'api'
2. Set the neccessary environment variables specified within the `deploy.sh` script, and run the `deploy.sh` script locally (ignoring lines 22-25 for now) to push up the container image to AWS ECR.
3. Within AWS EC2, create a new (internet-facing) Application Load Balancer, named 'api-load-balancer'. As well as the default security group, create a new security group 'api-alb-sg'. with inbound/outbound rules, and a new target group for routing for HTTP port 8000, with the health check at `/health`.
4. For the db setup, (i) create a another security group in AWS EC2, e.g. 'api-db-sg' - this has inbound HTTP rules on IPv4/IPv6, the custom 'api-alb-sg' and ssh ('My IP'), as well as adding an outbound HTTP rule for the custom 'api-alb-sg'. (ii) create a new database in AWS RDS (e.g. 'api-db') using PostgreSQL engine attaching the new 'api-db-sg', making note of the endpoint and username/password. 
5. Within AWS ECS (i) create a new task service definition, (ii) a new cluster, and (iii) a new task service within the cluster, specifying the relevant load balancer and target group.
6. Once successfully deployed, ssh into a running EC2 instance and run the migrations. This can be done by running `docker ps` to grab the api container id, and bash into the container `docker exec -it {container_id} bash`, to run the migrations with `alembic upgrade head`.
7. The endpoint specified by the load balancer in AWS can then be run in the browser, visiting `/health` and `/docs`
8. Further changes to the api can be deployed by running the `deploy.sh` script.

### Assumptions
The developer has an AWS account, as well as the AWS CLI and Docker (Desktop) installed locally.

### Considerations
Initial deployments using t2.micro EC2s within the ECS cluster failed, although scaling to use 3 t2.large EC2 resulted in successful deployments.

### Further work
Given more time, beyond the endpoint testing with postman, the integration and unit testing could be completed.
