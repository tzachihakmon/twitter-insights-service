# Repo Sturctue
1. Namespace for each component on our k8s cluster(cassandra,ingress, topic_repository_serrvice, topics_ingestor job, trends_engine_service, trends_public_api_service, tweets_public_api_service).
Each namespace contains docker and k8s sub dirs that are relevant for the k8s component.
2. Visualization_result_samples - dir with hundreds of visualized output of our service endpoints. 
3. two script(per trends api endpoints) to fetch topic trends insights from our service, create visualizations and save them to Visualization_result_samples dir. 
4. Ex summary. 

# Insights Engine K8s cluster Deployment proccess
## build images
From the repo root dir open pwsh an run:
### topics ingestor
- docker build --no-cache -f topics_ingestor_job/Dockerfile -t {your_docker_hub_user_name}/twitterinsightservice1-topics_ingestor-job .
### public- api
- docker build --no-cache -f trends_public_api_service/Dockerfile -t {your_docker_hub_user_name}/twitterinsightservice1-trends-public-api-service .
### trends-engine
docker build --no-cache -f trends_engine_service/Dockerfile -t {your_docker_hub_user_name}/twitterinsightservice1-trends-engine-service .
### topic-repository
docker build --no-cache -f topic_repository_service/Dockerfile -t {your_docker_hub_user_name}/twitterinsightservice1-topic-repository-service .

## Publish images to docker hub repository
### topics ingestor
- docker push {your_docke_hub_user_name}/twitterinsightservice1-topics_ingestor-job
### public- api
- docker push {your_docke_hub_user_name}/twitterinsightservice1-trends-public-api-service
### trends-engine
- docker push {your_docker_hub_user_name}/twitterinsightservice1-trends-engine-service
### topic-repository
- docker push {your_docker_hub_user_name}/twitterinsightservice1-topic-repository-service

# k8s steps:
Notice: containers images are fetched from tzachioy repository. If you would like to fetch them from your own docker hub repo, you should adjust k8s deployment files accordingly.
## initial cassandra cluster: 
kubectl apply -f cassandra/k8s/cassandra-statefulset.yaml
kubectl apply -f cassandra/k8s/cassandra-service.yaml

## Check that cassandra running gracefully with 
kubectl get pods 
kubectl get services

## deploy topic repository service
### Deploy
kubectl apply -f topic_repository_service/k8s/topic-repository-configmap.yaml
kubectl apply -f topic_repository_service/k8s/topic-repository-deployment.yaml
kubectl apply -f topic_repository_service/k8s/topic-repository-service-hpa.yaml
kubectl apply -f topic_repository_service/k8s/topic-repository-service.yaml

### check
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs trends-public-api-deployment-{some_prfix taken from get pods }
trends-public-api-configmap


## deploy topic ingestor job
### Deploy
kubectl apply -f topics_ingestor_job/k8s/topics-ingestor-configmap.yaml
kubectl apply -f topics_ingestor_job/k8s/topics-ingestor-job.yaml

### check
kubectl get jobs
kubectl get pods 
kubectl logs topics-ingestor{some_prfix taken from get pods }

## deploy public api service
### Deploy
kubectl apply -f trends_public_api_service/k8s/trends-public-api-configmap.yaml
kubectl apply -f trends_public_api_service/k8s/trends-public-api-deployment.yaml
kubectl apply -f trends_public_api_service/k8s/trends-public-api-hpa.yaml
kubectl apply -f trends_public_api_service/k8s/trends-public-api-service.yaml

### check
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs trends-public-api-deployment-{some_prfix taken from get pods }

## deploy trends engine service
### Deploy
kubectl apply -f trends_engine_service/k8s/trends-engine-configmap.yaml
kubectl apply -f trends_engine_service/k8s/trends-engine-deployment.yaml
kubectl apply -f trends_engine_service/k8s/trends-engine-service-hpa.yaml
kubectl apply -f trends_engine_service/k8s/trends-engine-service.yaml

### check
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs trends-public-api-deployment-{some_prfix taken from get pods }

## deploy ingress
### Pre-requisites:
1. From Adminstrator power shell - install chocolatey its package managment for windows: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

2. After u installed chocolatey install helm by it:
choco install kubernetes-helm

3. Install ngins-ingress:
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

### deployment 
1. install nginx-ingress Conroller:
helm install nginx-ingress ingress-nginx/ingress-nginx --namespace kube-system
2. kubectl apply -f ingress/k8s/ingressclass.yaml
3. kubectl apply -f ingress/k8s/ingress.yaml
4. check logs: 
kubectl get pods --all-namespaces
kubectl logs {nginx_pod_name} -n kube-system


## deploy tweets public api service
### Deploy
kubectl apply -f tweets_public_api_service/k8s/tweets-public-api-configmap.yaml
kubectl apply -f tweets_public_api_service/k8s/tweets-public-api-deployment.yaml
kubectl apply -f tweets_public_api_service/k8s/tweets-public-api-service.yaml