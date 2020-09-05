import sys
import pickle
from celery import Celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from fpdf import FPDF


logger = get_task_logger(__name__)
celery = Celery('celery_tasks')
celery.config_from_object('celeryconfig')


def is_task_active(fun, task_id, args):
    from celery.app.control import inspect
    if not args:
        args = "()"

    i = inspect()
    active_tasks = i.active()
    for _, tasks in active_tasks.items():
        for task in tasks:
            if task.get("id") == task_id:
                continue
            if task.get("name") == fun and task.get("args") == str(args):
                return True
    return False


def load_model():
    with open(f'model/clf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


model = load_model()


def get_task(task_id):
    """
    task_id의 결과를 얻는다.
    """
    return AsyncResult(task_id, app=celery)


def is_verified_data(data):
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for i in features:
        verified_data = i in data
    if verified_data == True:
        return True
    elif verified_data == False:
        return False


def get_predict_result(data):
    result = model.predict([[float(data[i]) for i in data]])
    return result


def make_pdf(data, result, task_id):     
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    line = 1
    logger.info('task_id: %s, Status: PROGRESS, Meta: starting to write to pdf', task_id)
    for key, val in data.items():
        text = key + ' = ' + str(val)
        pdf.cell(50, 10, txt=text, ln=line, align="C")
        line += 1
    pdf.cell(50, 10, txt='Predicted:' + result[0], ln=line, align="C")
    result_filename = 'report/'+str(task_id)+'.pdf'
    pdf.output(result_filename)
    return result_filename


@app.task()
def get_prediction_result_pdf(data):
    """ 
    celery를 통해 예측 결과를 pdf로 출력함
    """
    # 1. task_id를 받는다. task가 수행 가능상태인지 판단한다.
    function = f"{__name__}.{sys._getframe().f_code.co_name}"
    task_id = None
    if celery.current_task:
        task_id = celery.current_task.request.id
    
    if task_id and is_task_active(function, task_id, None):
        log_data = {
        "function": function,
        "message": "Starting job.",
        "task_id": task_id,
        }
        log_data["message"] = "Skipping task: Task is already active"
        logger.debug(log_data)
        return
    celery.current_task.update_state(state='PROGRESS', meta={'current':0.1})
    logger.info('task_id: %s, Status: PROGRESS, Meta: prediction started', task_id)

    # 2. 데이터 검증을 한다.
    if is_verified_data(data) != True:
        celery.current_task.update_state(state='FAILURE', meta={'current': 1})
        logger.info('task_id: %s, Status: FAILURE, Meta: data format is wrong', task_id)
        return "FAIL"
    celery.current_task.update_state(state='PROGRESS', meta={'current': 0.2})
    logger.info('task_id: %s, Status: PROGRESS, Meta: data verified', task_id)

    # 3. 결과값을 예측을 한다.
    result = get_predict_result(data)
    celery.current_task.update_state(state='PROGRESS', meta={'current': 0.6})
    logger.info('task_id: {%s}, Status: PROGRESS, Meta: model predicted = %s ', task_id, result)
    
    # 4. PDF를 생성 한다.
    result_filename = make_pdf(data, result, task_id)
    logger.info('task_id: %s, Status: PROGRESS, Meta: written to pdf', task_id)
    celery.current_task.update_state(state='PROGRESS', meta={'current': 0.9})
    return result_filename
