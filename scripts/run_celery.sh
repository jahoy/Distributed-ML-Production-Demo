#!/bin/sh
cd app  
su -m app -c "celery -A celery_tasks worker --loglevel INFO" 