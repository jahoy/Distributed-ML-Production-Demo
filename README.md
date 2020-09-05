# DISTRIBUTED-ML-PRODUCTION-DEMO

FastAPI, Celery, RabbitMQ, Redis를 이용한 머신러닝 모델 예측 작업 수행 및 분산 처리 demo


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

## 실행법
    docker-compose build
    docker-compose up
    docker-compose scale worker=N
