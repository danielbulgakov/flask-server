sudo service postgresql stop
sudo systemctl stop postgresql

cd /root/src/docker/database
docker-compose up -d