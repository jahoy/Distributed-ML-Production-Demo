#!/bin/sh
cd app
su -m app -c "uvicorn app:app --reload"
