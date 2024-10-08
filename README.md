 # Google Play Store Dashboard

![Dashboard Screenshot](assets/share_google_play_logo.png) <!-- Google Playstore Image -->

## Project Overview
This project was developed at Unified Mentor by **Rajat Singh**. The goal is to create an interactive dashboard using Dash to explore Google Play Store data.

## Project Structure
- **dashboar.py**: Main application file containing the layout and logic for the Dash app.
- **data_ingestion.py**: Contains functions for ingesting data from MongoDB.
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



