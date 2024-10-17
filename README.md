 # Google Play Store Dashboard

 ## Create python environemnt 3.12 for this project

![Dashboard Screenshot](assets/share_google_play_logo.png) <!-- Google Playstore Image -->

## Project Overview
This project was developed at Unified Mentor by **Rajat Singh**. The goal is to create an interactive dashboard using Dash to explore Google Play Store data.

## Project Structure
- **dashboar.py**: Main application file containing the layout and logic for the Dash app.
- **data_dump.py**: Script used to dump cleaned datasets into MongoDB.
- **google_rearch.ipynb**: Jupyter notebook where Exploratory Data Analysis (EDA) was performed using Sweetviz. 
- **datasets/**: Directory containing all datasets used in the project.
- **assets/**: Contains CSS styles and images for the dashboard.
- **Project demo/**: Folder Contains Project demo vedio. 
- **Screeshot/**: Folder Contains Screenshots of  app.
- **requirements.txt/**: Contains all modules require for this Project.

## Features
- **Data Ingestion**: Connects to MongoDB and retrieves the dataset.
- **Exploratory Data Analysis**: Conducted using Sweetviz for basic observations.
- **Data Merging**: Merges Google app dataset with user reviews for comprehensive analysis.
- **Interactive Dashboard**: Built using Dash to visualize various aspects of the data, including plots and metrics.

## Setup Instructions
1. Clone the repository.
2. Create a `.env` file to store sensitive MongoDB connection information. 
3. Create a `Procfile` file for Deployment.


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
docker run -p  8501:8501 google/app
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
docker tag google/app:latest docker_username/google-app:latest
```

```bash
docker push  docker_username/google-app:latest
```

```bash
docker rmi google/app:latest
```

```bash
docker pull google/app
```











