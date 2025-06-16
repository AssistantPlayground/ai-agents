#!/bin/sh
set -e

# Waiting for MinIO
echo "Waiting for MinIO..."
until mc admin info minio > /dev/null 2>&1; do
  echo "MinIO is not ready yet - setting up connection..."
  mc alias set minio http://minio:9000 admin password
  sleep 3
done
echo "MinIO started and ready to work!"

# Create necessary buckets
echo "Creating necessary buckets..."
mc mb --ignore-existing minio/documents
mc mb --ignore-existing minio/embeddings

# Setting up AMQP for notifications
echo "Setting up AMQP for notifications..."
mc admin config set minio/ notify_amqp:minio \
  url="amqp://guest:guest@rabbitmq:5672" \
  comment="Setting up MinIO notifications through RabbitMQ"

# Applying configuration changes
echo "Applying configuration changes..."
mc admin service restart minio/

# Waiting for MinIO restart
echo "Waiting for MinIO restart..."
sleep 3

# Setting up notifications for buckets
echo "Setting up notifications for buckets..."
mc event add minio/documents arn:minio:sqs::minio:amqp --event put,delete
mc event add minio/embeddings arn:minio:sqs::minio:amqp --event put,delete

echo "MinIO with AMQP setup completed successfully!"
