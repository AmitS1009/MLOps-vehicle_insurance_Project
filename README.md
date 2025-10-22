# 🚗 MLOps Project - Vehicle Insurance Data Pipeline

Welcome to this **end-to-end MLOps project**, showcasing a fully automated and production-ready pipeline for managing **vehicle insurance data** using **Azure Cloud**, **Docker**, and **GitHub Actions**.
This project demonstrates a real-world workflow — from data ingestion and preprocessing to model training, evaluation, and web deployment.

---

## 📁 Project Setup and Structure

### Step 1: Project Template

* Execute `template.py` to automatically create the full project structure (folders, modules, and placeholders).

### Step 2: Package Management

* Set up package imports using `setup.py` and `pyproject.toml`.
* Refer to `crashcourse.txt` for a short tutorial on how they work.

### Step 3: Virtual Environment & Dependencies

```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
```

Verify local package installations:

```bash
pip list
```

---

## 📊 MongoDB Setup and Data Management

### Step 4: MongoDB Atlas Configuration

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Allow access from all IPs (`0.0.0.0/0`) and create database credentials.
3. Copy your connection string and replace `<password>`.

### Step 5: Pushing Data to MongoDB

1. Inside the `notebook` folder, open `mongoDB_demo.ipynb`.
2. Use it to upload raw vehicle insurance data to MongoDB Atlas.
3. Verify uploaded data under *Browse Collections* in the Atlas dashboard.

---

## 🧩 Logging, Exception Handling, and EDA

### Step 6: Logging and Exception Handling

* Implemented in dedicated modules under `logger` and `exception`.
* Tested through `demo.py`.

### Step 7: Exploratory Data Analysis (EDA) & Feature Engineering

* Conducted in Jupyter notebooks under `notebook/EDA` and `notebook/FeatureEngg`.

---

## 📥 Data Ingestion and Environment Variables

### Step 8: Data Ingestion Pipeline

* Developed under `components/data_ingestion.py`.
* Configurations managed through `entity/config_entity.py` and `entity/artifact_entity.py`.

### Setting Environment Variables

```bash
# For Bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/"
```

---

## 🔍 Data Validation, Transformation & Model Training

### Step 9: Data Validation

* Schema defined in `config/schema.yaml`.
* Validation utilities located in `utils/main_utils.py`.

### Step 10: Data Transformation

* Implemented in `components/data_transformation.py`.
* Uses custom transformer and estimator logic in `entity/estimator.py`.

### Step 11: Model Training

* Model training handled by `components/model_trainer.py`.
* Includes training, metrics computation, and saving serialized models.

---

## ☁️ **Azure Integration & Deployment**

### Step 12: Azure Storage Setup

* Replaced AWS S3 with **Azure Blob Storage** for storing and retrieving models.
* Implemented in `src/cloud_storage/azure_storage.py`.

### Environment Variable

```bash
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=<storage-name>;AccountKey=..."
```

### Step 13: Azure Container Registry (ACR)

* Used **Azure Container Registry (ACR)** to store Docker images.

```bash
docker build -t <ACR-username>.azurecr.io/vehicle-insurance:latest .
docker push <ACR-username>.azurecr.io/vehicle-insurance:latest
```

### Step 14: Azure Virtual Machine (VM) Deployment

1. Created an Ubuntu VM on Azure.
2. Installed Docker and GitHub Actions Runner.
3. Deployed the app using:

   ```bash
   docker run -d \
     -p 5000:5000 \
     --name vehicle-insurance \
     -e AZURE_STORAGE_CONNECTION_STRING="..." \
     mlopsregistry4321.azurecr.io/vehicle-insurance:latest
   ```
4. Visit your live app at:

   ```
   http://<your-vm-public-ip>:5000
   ```

---

## ⚙️ CI/CD Automation with GitHub Actions

### Step 15: GitHub Actions Workflow

* Fully automated CI/CD pipeline using self-hosted Azure VM runner.
* Workflow triggers on every push to `main`.

**GitHub Secrets:**

```
AZURE_CREDENTIALS
AZURE_REGISTRY_USERNAME
AZURE_REGISTRY_PASSWORD
```

---

## 🧠 Model Evaluation & Prediction Pipeline

### Step 16: Model Evaluation & Pusher

* Implemented under `components/model_evaluation.py` and `pipline/prediction_pipeline.py`.
* Final predictions served through a **Flask web app (`app.py`)**.

### Step 17: Web Interface

* Frontend built using HTML/CSS under `templates/` and `static/`.

---

## 🎯 Workflow Summary

1. **Data Ingestion** → **Data Validation** → **Data Transformation**
2. **Model Training** → **Model Evaluation** → **Azure Deployment**
3. **CI/CD** with Docker + GitHub Actions + Azure VM + ACR

---

## 🏁 Final Outcome

✅ Fully working **web app** hosted on **Azure VM**
✅ Containerized with **Docker**
✅ Models stored & retrieved from **Azure Blob Storage**
✅ Continuous integration & deployment using **GitHub Actions**

---

## 💬 Connect

If this project inspires you or helps you prepare for interviews, feel free to connect and share feedback! 🚀

---
