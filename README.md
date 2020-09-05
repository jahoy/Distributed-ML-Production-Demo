# DISTRIBUTED-ML-PRODUCTION-DEMO

FastAPI, Celery, RabbitMQ, Redis를 이용한 머신러닝 모델 예측 작업 수행 및 분산 처리 demo
![celery](https://user-images.githubusercontent.com/50973416/92310540-71de4800-efea-11ea-8893-e594b211f330.png)

fastapi(웹)을 통해 request를 날릴 때마다 prediction요청이 진행되고, 이때 RabbitMQ에 큐에 일감으로 하나하나 차곡차곡 들어간다.
celery worker들을 그 일감들을 하나하나 분배받으며 prediction결과를 pdf로 바꾸는 작업(delay가 많은 작업으로 분산처리)을 한 뒤 redis에 저장된다. 
결과물은 redis로부터 다시 받아볼 수 있다.


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
