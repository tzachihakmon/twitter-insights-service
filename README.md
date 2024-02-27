This is my first flask k8s app

# Docker images creation:
From the repo root dir open pwsh an run:

## build images
### ingestor
- docker build -f topics_ingestor/Dockerfile.topics_ingestor -t {your_docker_hub_user_name}/twitterinsightservice1-topics_ingestor-job .
### public- api
- docker build -f trends_public_api_service/Dockerfile.topics_public_api -t {your_docke_hub_user_name}/twitterinsightservice1-trends-public-api-servic
### trends-engine
docker build --no-cache -f trends_engine_service/Dockerfile.trends_engine -t tzachioy/twitterinsightservice1-trends-engine-service .

## Publish images to docker hub repository
### ingestor
- docker push {your_docke_hub_user_name}/twitterinsightservice1-topics_ingestor-job
### public- api
- docker push {your_docke_hub_user_name}/twitterinsightservice1-trends-public-api-servic
### trends-engine
- docker push tzachioy/twitterinsightservice1-trends-engine-service
# k8s steps:
## initial cassandra cluster: 
kubectl apply -f k8s/cassandra-statefulset.yaml

## Check that cassandra running gracefully with 
kubectl get pods 
kubectl get services

## initial topic ingestor job
kubectl apply -f k8s/topics-ingestor-job.yaml
kubectl get jobs
kubectl get pods 
kubectl logs topics-ingestor{some_prfix taken from get pods }

## initial public api service
kubectl apply -f k8s/trends-public-api-deployment.yaml
kubectl apply -f k8s/trends-public-api-service.yaml
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs trends-public-api-deployment-{some_prfix taken from get pods }


## initial test engine service
kubectl apply -f k8s/trends-engine-deployment.yaml
kubectl apply -f k8s/trends-engine-service.yaml
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs trends-public-api-deployment-{some_prfix taken from get pods }