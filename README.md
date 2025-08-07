# Smart Parking Management System

A comprehensive parking management system with role-based access control and automated fee calculation.

## Installation Guide

### Prerequisites
- Python 3.8 or higher

### Step 1: Clone the Repository
```bash
git clone https://github.com/zombieTDV/Smart_Parking_Management_System.git
cd smart_parking_management_system
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv ENV

# Activate virtual environment
# On Windows:
ENV\Scripts\activate.bat
# On macOS/Linux:
source ENV/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

## Project Structure

```
smart_parking_management_system/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── config/
│   └── config.yaml
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── parking_slot.py
│   │   └── transaction.py
│   │   
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── parking_service.py
│   │   ├── fee_calculator.py
│   │   └── report_service.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── admin_controller.py
│   │   ├── attendant_controller.py
│   │   └── owner_controller.py
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   └── menu.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
│
├── docs/
│   ├── flowchart.png
│   └── class_descriptions.md
│
├── screenshots/
│   └── role_based_interactions.png
│
└── tests/
    ├── conftest.py
    ├── test_user.py
    ├── test_parking_slot.py
    └── test_transaction.py
