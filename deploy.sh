#!/bin/sh

# variables
aws_region="$AWS_REGION"
aws_account_id="$AWS_ACCOUNT_ID"
aws_ecr_name="$AWS_ECR_NAME"
aws_cluster_name="$AWS_CLUSTER_NAME"
aws_service_name="$AWS_SERVICE_NAME"

# pre-build
echo "authenticating the docker cli to use the ECR registry..."
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

# build
echo "building image..."
docker build -f project/Dockerfile.production --platform=linux/amd64 -t $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev ./project/

# post-build
echo "pushing image to AWS ECR..."
docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev

echo "updating ECS service..."
aws ecs update-service --cluster $aws_cluster_name --service $aws_service_name --force-new-deployment

echo "complete!"