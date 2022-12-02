from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
import shutil
import time
import os


logger = get_task_logger(__name__)


@shared_task
def delete_results():
    logger.info("Files are being removed")
    walk_tuple = next(os.walk(os.path.join(settings.MEDIA_ROOT, 'results')))
    root = walk_tuple[0]
    dirs = walk_tuple[1]
    for dir in dirs:
        result_dir = os.path.join(root, dir)
        age_s = time.time() - os.path.getmtime(result_dir)

        # The dir is removed if it's older than an hour
        if age_s > 60 * 60:
            try:
                shutil.rmtree(result_dir)
            except:
                logger.info(f'ERROR: results directory {result_dir} could not be removed. '
                            f'File age: {age_s} seconds')
