#!/usr/bin/env bash

# CREATED: 2018-11-27
# AUTHORS: Dmitriy Repin drepin@slb.com
# MAINTAINERS: 
# This script perform a deployment of drepin-service to a GKE cluster

if [ ! -f ./drepin-service.Dockerfile ]; then
    echo "***ERROR: The script must be run from the project root directory"
    exit 1
fi 

if [ -z "$1" ]; then 
    MODE="deploy"
else
    if [ $MODE == "deploy" ] || [ $MODE == "clean" ]; then
        echo "***ERROR: Invalid mode"
        exit 1
    fi
fi


# TODO: Properly expose variables as parameters
export PROJECT_NAME=AAAAAA
export SERVICE_NAME=drepin-service
export CLUSTER_NAME=drepin-cluster
export HOST_NAME=drepin-service.com

#---------------------------------------------
# Clean up
#---------------------------------------------
if [ $MODE == "clean" ]; then
    kubectl delete ingress $SERVICE_NAME-ingress
    kubectl delete hpa $SERVICE_NAME-hpa
    kubectl delete service $SERVICE_NAME
    kubectl delete deployments $SERVICE_NAME-worker

    kubectl delete secret $SERVICE_NAME-tls-secret
    kubectl delete secret $SERVICE_NAME-oauth-secret

    gcloud compute firewall-rules delete $SERVICE_NAME-iap-allow-health-checks
    gcloud container clusters delete $CLUSTER_NAME --zone us-central1-c
    gcloud compute addresses delete $SERVICE_NAME-static-ip --global
    gcloud compute ssl-certificates create $SERVICE_NAME-ssl-certificate 

    exit 0
fi

# Define a health check firewall rule to be used by the cluster
gcloud compute firewall-rules create $CLUSTER_NAME-iap-allow-health-checks \
    --network default \
    --action ALLOW \
    --direction INGRESS \
    --source-ranges 35.191.0.0/16,130.211.0.0/22 \
    --target-tags $CLUSTER_NAME-allow-health-checks \
    --rules tcp

#------------------------------------------
# Create a KGE cluster
# NOTE: minimal GKE version is 1.10.5-gke.3. (use the following command to check):
#    kubectl version --short=true 
#------------------------------------------
gcloud container clusters create $CLUSTER_NAME \
    --machine-type n1-standard-1 \
    --num-nodes 3 \
    --no-enable-basic-auth \
    --no-issue-client-certificate \
    --enable-ip-alias \
    --zone us-central1-c \
    --cluster-version latest \
    --enable-autoupgrade \
    --tags=$CLUSTER_NAME-allow-health-checks  
gcloud container clusters get-credentials $CLUSTER_NAME --zone us-central1-c

#------------------------------------------
# Set IP and domain for a service
#------------------------------------------
# Reserve a static IP address for the service
gcloud compute addresses create $SERVICE_NAME-static-ip --global
# Reserve a domain name and set it to resolve this IP address
echo -e "\033[0;31mTODO: Reserve a domain name and set it to resolve this IP address\033[0m"
gcloud compute addresses describe drepin-service-static-ip --global | grep "address: "
# godaddy.com -> DNS -> Check the 'A'-type record

#------------------------------------------
# Create TLS secret to use for HTTPS
#------------------------------------------
# Generate the key
mkdir -p tls && cd tls/
openssl genrsa -out tls.key 2048
openssl req -new -key tls.key -out tls.csr -subj \
    "/C=US/ST=Texas/L=Houston/O=Repin Ltd/OU=Vostok/emailAddress=drepin@hotmail.com/CN=drepin-service.com"
# Generate self-signed sertificate
openssl x509 -req -days 365 -in tls.csr -signkey tls.key -out tls.crt
gcloud compute ssl-certificates create $SERVICE_NAME-ssl-certificate --certificate tls.crt --private-key tls.key
# Generate  Kubernetes tls sertificate secret
kubectl create secret tls $SERVICE_NAME-tls-secret --key tls.key --cert tls.crt
# Clean Up: remove tls.key tls.csr tls.crt
cd .. && rm -rf tls/

#------------------------------------------
# Create an OAuth secret to use for HTTPS Authorization
#------------------------------------------
# Using API & Services -> Credentials -> OAuth 2.0 client IDs @ $PROJECT for drepin-service
kubectl create secret generic $SERVICE_NAME-oauth-secret \
    --from-literal=client_id=783663625239-8qnbblrah68geav3dl1dq2amli7n1p3g.apps.googleusercontent.com \
    --from-literal=client_secret=hD9_OwDw4iViM8g0_6_AqvYX


#--------------------------------------------
# Deploy
#--------------------------------------------
printf  "# Generated configuration file\n" > drepin-service.yaml
envsubst <  drepin-service.deployment.yaml >>  drepin-service.yaml
envsubst <  drepin-service.service.yaml    >>  drepin-service.yaml
envsubst <  drepin-service.ingress.yaml    >>  drepin-service.yaml
envsubst <  drepin-service.hpa.yaml        >>  drepin-service.yaml

kubectl apply -f  drepin-service.yaml

echo -e "\033[0;31mTODO: Grant the 'Cloud IAP->IAP-Secured Web App User' access permissions:\033[0m"
echo -e "\033[0;31m   Security->Identity-Aware-Proxy->default/drepin- drepin-service\033[0m"
## NOTE: You can grant permanent access permission to ALL IAPs in the project as following
# export PROJECT_ID=783663625239
# export SERVICE_ID=k8s1-0f4aa0a7-default-drepin-service-8080-c97fcd91
# gcloud projects add-iam-policy-binding $PROJECT_ID \
#     --role=roles/iap.httpsResourceAccessor \
#     --member=serviceAccount:auto-test@project.iam.gserviceaccount.com
## NOTE: To grant access permission to a specific service, you can do
##       however, this will require OAuth2 Google Bearer Token (see Postman.md)
## POST https://iap.googleapis.com/v1beta1/projects/${PROJECT_ID}/iap_web/compute/services/${SERVICE_ID}:setIamPolicy
##      Body: iap-policy.json
# curl -s \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#     -T iap-policy.json \
#     --verbose \
#     https://iap.googleapis.com/v1beta1/projects/${PROJECT_ID}/iap_web/compute/services/${SERVICE_ID}:setIamPolicy
