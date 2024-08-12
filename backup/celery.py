import os
from datetime import timedelta
from celery import Celery
from backup.tasks import backup_postgres_and_upload
from celery.schedules import crontab
from dotenv import load_dotenv

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')

app = Celery('backupPG')

# Load environment variables from .env file
load_dotenv()


# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls the first backup task for 'infifteen' every 10 seconds
    sender.add_periodic_task(
        timedelta(seconds=10),
        backup_postgres_and_upload.s(
            database_name=os.environ.get('DATABASE_NAME1'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
            host=os.environ.get('DATABASE_HOST'),
            port=5432,
            backup_dir='.'
        ),
        name='Backup PostgreSQL infifteen every 10 seconds'
    )

    # Calls the second backup task for 'bloggy' every 10 seconds
    sender.add_periodic_task(
        timedelta(seconds=10),
        backup_postgres_and_upload.s(
            database_name=os.environ.get('DATABASE_NAME2'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
            host=os.environ.get('DATABASE_HOST'),
            port=5432,
            backup_dir='.'
        ),
        name='Backup PostgreSQL bloggy every 10 seconds'
    )

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')






#FOR WEEKLY TASKS


# import os
# from datetime import timedelta
# from celery import Celery
# from backup.tasks import backup_postgres_and_upload
# from celery.schedules import crontab
# from dotenv import load_dotenv

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')

# app = Celery('backupPG')

# # Load environment variables from .env file
# load_dotenv()

# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Schedule the first backup task for 'infifteen' every week
#     sender.add_periodic_task(
#         crontab(hour=0, minute=0, day_of_week='sunday'),  # This schedules the task every Sunday at midnight
#         backup_postgres_and_upload.s(
#             database_name=os.environ.get('DATABASE_NAME1'),
#             user=os.environ.get('DATABASE_USER'),
#             password=os.environ.get('DATABASE_PASSWORD'),
#             host=os.environ.get('DATABASE_HOST'),
#             port=5432,
#             backup_dir='.'
#         ),
#         name='Backup PostgreSQL infifteen every Sunday at midnight'
#     )

#     # Schedule the second backup task for 'bloggy' every week
#     sender.add_periodic_task(
#         crontab(hour=0, minute=0, day_of_week='sunday'),  # This schedules the task every Sunday at midnight
#         backup_postgres_and_upload.s(
#             database_name=os.environ.get('DATABASE_NAME2'),
#             user=os.environ.get('DATABASE_USER'),
#             password=os.environ.get('DATABASE_PASSWORD'),
#             host=os.environ.get('DATABASE_HOST'),
#             port=5432,
#             backup_dir='.'
#         ),
#         name='Backup PostgreSQL bloggy every Sunday at midnight'
#     )

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

