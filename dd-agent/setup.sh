#/bin/bash 

# Create the Datadog API Secret 
read -sp "Enter your API key: " API_KEY
echo 

# Update Helm
helm repo add datadog https://helm.datadoghq.com
helm repo update
kubectl create secret generic datadog-secret --from-literal api-key=$API_KEY

