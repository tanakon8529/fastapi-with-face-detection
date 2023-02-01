## To deploy with docker-compose command
To install/update this application. 
Run (if you see running and check error!!)

    docker-compose build

and (if you see running and check error!!)

     docker-compose up

Or >>build and up in one line<< (If you don't see running and check error.)

    Run docker-compose up --build -d 

To stop-application. 

    docker-compose down 

To uninstall this application. 

    docker stack rm <stack name>

## ============ ORIGINAL ============ ##
## Installation
run these command to install this project.

### 1. Clone repo
```bash
git clone https://github.com/ratthapon/face-detection
```

### 2. Setup virtual environment
```bash
python3 -m venv venv
```

### 3. Install dependencies
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Deployment


### 1. Load installed dependencies
```bash
source venv/bin/activate
```

### 2. Start engine in a terminal manner 
```bash
python3 face_detection_engine.py
```
