# ai-cloud-cost-analyzer

## 📌 Overview
This project helps you understand and track your AWS cloud spending in a simple way. It connects to AWS Cost Explorer API, pulls real billing data, and turns it into useful insights like service-wise cost breakdown and future cost estimation.

## ⚙️ What it does
- Connects to AWS and fetches real cost data  
- Breaks down spending by AWS services (EC2, S3, RDS, etc.)  
- Gives a clear view of where your cloud money is going  
- Uses basic ML to estimate future costs based on past usage  
- Exposes data through a FastAPI backend  

## 🛠️ Tech Stack
- Python  
- FastAPI  
- Boto3 (AWS SDK)  
- Pandas  
- Scikit-learn (for prediction)  

## 🚀 How to Run the Project

```bash
pip install -r requirements.txt
uvicorn main:app --reload
