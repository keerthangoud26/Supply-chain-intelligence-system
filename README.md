# SupplySense AI – Real-Time Supply Chain Intelligence Platform

## Overview

SupplySense AI is an enterprise-grade AI-powered supply chain intelligence platform built to monitor, analyze, and optimize supply chain operations in real time.

The platform combines real-time event streaming, machine learning forecasting, anomaly detection, logistics analytics, supplier quality monitoring, and inventory intelligence into a unified dashboard.

It simulates how modern organizations use distributed systems and AI to improve operational efficiency and business decision-making.

---

## Key Features

### Real-Time Dashboard Analytics

* Live KPI monitoring for revenue, products, shipping costs, supplier quality, and inventory performance
* Auto-refreshing dashboard powered by API polling

### Inventory Intelligence

* SKU-level stock monitoring
* Low-stock alerts for critical inventory
* Inventory health scoring system

### Supplier Intelligence

* Supplier defect rate analysis
* Supplier performance benchmarking
* Quality anomaly monitoring

### Logistics Analytics

* Transportation mode cost analysis
* Shipping cost optimization insights
* Route-based logistics intelligence

### AI Prediction Engine

* Machine learning based revenue forecasting
* Predictive analytics for future supply trends
* Forecast visualization dashboard

### Anomaly Detection Engine

* Detection of unusual logistics cost spikes
* Inventory shortage anomaly detection
* Supplier defect anomaly alerts

### Real-Time Data Streaming

* Apache Kafka producer-consumer architecture
* Live sales events streamed into PostgreSQL
* Dashboard updates automatically every 5 seconds

### Reports & Insights

* Historical operational reporting
* Performance trend analytics
* Business intelligence visualizations

---

## System Architecture

Producer Service
↓
Apache Kafka Event Streaming
↓
Kafka Consumer Service
↓
PostgreSQL Database
↓
FastAPI Backend APIs
↓
React Frontend Dashboard
↓
Real-Time Business Analytics

---

## Tech Stack

### Frontend

* React
* TypeScript
* Tailwind CSS
* Recharts
* Lucide React Icons

### Backend

* FastAPI
* REST APIs
* Python

### Database

* PostgreSQL

### Streaming Infrastructure

* Apache Kafka
* Zookeeper

### DevOps / Infrastructure

* Docker
* MinIO Object Storage

### Machine Learning / AI

* Scikit-learn
* Predictive Revenue Forecasting
* Anomaly Detection Engine

---

## Major Engineering Concepts Implemented

* Distributed Event Streaming Architecture
* Producer Consumer Architecture
* Real-Time Data Processing Pipeline
* API Driven Dashboard Architecture
* Database Analytics with SQL
* Machine Learning Forecasting Models
* Enterprise Dashboard Design
* Dockerized Infrastructure Deployment

---

## Project Workflow

1. Kafka Producer generates live sales events
2. Kafka Consumer reads events in real time
3. Consumer inserts sales records into PostgreSQL
4. FastAPI APIs fetch live analytics data
5. React frontend polls APIs every 5 seconds
6. Dashboard updates automatically without refresh
7. ML engine generates revenue predictions
8. Anomaly engine detects operational irregularities

---

## Screenshots
* Dashboard Overview
<img width="1913" height="1145" alt="image" src="https://github.com/user-attachments/assets/f06e9f1a-0660-4094-b97f-791defa9e295" />

* Inventory Intelligence
  <img width="1918" height="1091" alt="image" src="https://github.com/user-attachments/assets/4f619121-f987-4142-9d3a-4470b886448b" />

* Supplier Analytics
  <img width="1918" height="1087" alt="image" src="https://github.com/user-attachments/assets/00bda07b-816a-4339-89f2-7001cfdacf42" />

* Logistics Analytics
  <img width="1917" height="1091" alt="image" src="https://github.com/user-attachments/assets/62b8ff96-835e-4b0c-bbe0-1991df72561a" />

* AI Prediction Engine
  <img width="1918" height="1087" alt="image" src="https://github.com/user-attachments/assets/a46b5ea6-70df-41d6-8d91-fac31a6b90cd" />

* Anomaly Detection Engine
  <img width="1915" height="1091" alt="image" src="https://github.com/user-attachments/assets/317b7ae3-461f-4c17-a47b-75a8ab994873" />

* Settings Page
  <img width="1918" height="1092" alt="image" src="https://github.com/user-attachments/assets/68ded9f4-5d24-4dec-9445-7a61aaf61aca" />


---

## Run Locally

### Clone Repository

https://github.com/keerthangoud26/Supply-chain-intelligence-system.git

### Install Frontend Dependencies

npm install

### Run Frontend

npm run dev

### Run Backend

uvicorn main:app --reload

### Start Docker Services

docker-compose up -d

### Run Kafka Consumer

python kafka_consumer.py

### Run Kafka Producer

python kafka_producer.py

---

## Future Improvements

* Cloud deployment on AWS
* WebSocket-based live updates
* Authentication and user roles
* Multi-user enterprise access
* AI-based supply chain optimization recommendations
* Automated procurement intelligence

---

## Author

Keerthan Goud

Built as a full-stack AI + Data Engineering + Distributed Systems project.
