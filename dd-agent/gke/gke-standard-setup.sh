#/bin/bash 

# Create the Datadog API Secret 
read -sp "Enter your API key: " API_KEY
echo 

# Update Helm
helm repo add datadog https://helm.datadoghq.com
kubectl create namespace datadog

#required for introspection.enabled=true required for some reason
helm install datadog-operator datadog/datadog-operator --set introspection.enabled=true -n datadog
kubectl create secret generic datadog-secret --from-literal api-key=$API_KEY -n datadog
k apply -f datadog-values.yaml
