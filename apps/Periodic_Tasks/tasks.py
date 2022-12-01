from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
import shutil
import os

logger = get_task_logger(__name__)


@shared_task
def delete_results():
    logger.info("The task is called right now")

    # todo change loop (look at comment below)
    # os.walk geeft ('/home/app/media/results', ['5a51f714-923c-4792-b027-c34904756202', 'ec040ef5-f7c9-4532-b4df-05c82113683e'], ['.gitkeep'])
    for result_dir in os.walk(os.path.join(settings.MEDIA_ROOT, 'results')):
        logger.info(result_dir)
        try:
            shutil.rmtree(result_dir)
        except:
            print('ERROR: results could not be removed')
