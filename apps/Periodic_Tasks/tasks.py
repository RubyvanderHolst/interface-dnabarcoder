from celery import shared_task
from celery.utils.log import get_task_logger
import shutil
import time
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User

from apps.Authentication.models import TaskInfo


'''
The schedule of these tasks are defined in settings.py under 
CELERY_BEAT_SCHEDULE
'''


logger = get_task_logger(__name__)


@shared_task
def delete_results():
    logger.info("Result files are being removed")
    walk_tuple = next(os.walk(os.path.join(settings.MEDIA_ROOT, 'results')))
    root = walk_tuple[0]
    dirs = walk_tuple[1]
    for dir in dirs:
        result_dir = os.path.join(root, dir)
        age_s = time.time() - os.path.getmtime(result_dir)

        # The dir is removed if it's older than a day
        if age_s > 60 * 60 * 24:
            try:
                shutil.rmtree(result_dir)
            except:
                logger.info(f'ERROR: results directory {result_dir} could not be removed. '
                            f'File age: {age_s} seconds')


def remove_account(task_id):
    try:
        user = User.objects.get(username=task_id)
        user.delete()
    except User.DoesNotExist:
        print(f"User {task_id} does not exist, cannot be deleted")


@shared_task
def delete_uploaded():
    files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'uploaded'))
    files.remove('.gitkeep')
    for file in files:
        full_path = os.path.join(settings.MEDIA_ROOT, 'uploaded', file)
        age_s = time.time() - os.path.getmtime(full_path)

        # The file is removed if it's older than a day
        if age_s > 60 * 60 * 24:
            try:
                os.remove(full_path)
            except:
                logger.info(f'ERROR: {full_path} could not be removed')


@shared_task
def clean_db():
    threshold_1day_old = datetime.now() - timedelta(hours=24)

    old_tasks = TaskInfo.objects.filter(time_creation__lt=threshold_1day_old)
    if old_tasks.exists():
        for task in old_tasks.iterator():
            user = User.objects.get(id=task.user_id)
            user.delete()
