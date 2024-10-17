# Streamlit app Docker Image

## 1. Login with your AWS console and launch an EC2 instance
## 2. Run the following commands

Note: Do the port mapping to this port:- 8501

```bash
sudo apt-get update -y

sudo apt-get upgrade

#Install Docker

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```

```bash
git clone https://github.com/RJSINGH64/google_playstore.git
```

```bash
docker build -t google/app:latest . 
```

```bash
docker images -a  
```

```bash
docker run -d  8501:8501 google/app
```

```bash
docker ps  
```

```bash
docker stop container_id
```

```bash
docker rm $(docker ps -a -q)
```

```bash
docker login 
```

```bash
docker push google/app:latest
```

```bash
docker rmi google/app:latest
```

```bash
docker pull google/app
```






