# This script uses docker exec to manually create the user and database
# This is necessary because the Docker volume persists the OLD configuration
# and ignores the new environment variables in docker-compose.yml.

Write-Host "Creating user 'agent'..."
docker exec postgres psql -U postgres -d postgres -c "CREATE USER agent WITH PASSWORD '123';"

Write-Host "Creating database 'amarthafin'..."
docker exec postgres psql -U postgres -d postgres -c "CREATE DATABASE amarthafin OWNER agent;"

Write-Host "Granting privileges..."
docker exec postgres psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE amarthafin TO agent;"

Write-Host "Done! You should now be able to connect with agent/123/amarthafin."
