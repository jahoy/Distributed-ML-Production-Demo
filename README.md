# DISTRIBUTED-ML-PRODUCTION-DEMO

FastAPI, Celery, RabbitMQ, Redis를 이용한 머신러닝 모델 예측 작업 수행 및 분산 처리 demo
![celery](https://user-images.githubusercontent.com/50973416/92310540-71de4800-efea-11ea-8893-e594b211f330.png)



## 파일 구조
    ├── Dockerfile
    ├── README.md
    ├── app
    │   ├── app.py
    │   ├── celery_tasks.py
    │   ├── celeryconfig.py
    │   ├── train_model.py
    │   ├── model
    │   ├── report
    │   ├── templates
    │   │   ├── home.html
    │   │   └── index.html
    ├── docker-compose.yml
    ├── iris.csv
    ├── requirements.txt
    └── scripts
        ├── run_celery.sh
        └── run_web.sh

## 준비
    virtualenv -p python3.7 .env

    source .env/bin/activate

    pip3 install -r requirements.txt


## 실행법
    docker-compose build
    
    docker-compose up
    
    docker-compose scale worker=N
