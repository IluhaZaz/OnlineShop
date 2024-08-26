#!/bin/bash

cd src

if [[ "${1}" == "celery" ]]; then
  celery --app=tasks.email_task:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=tasks.email_task:celery flower
 fi