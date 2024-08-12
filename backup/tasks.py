from __future__ import print_function
from celery import shared_task
import os
import subprocess
from datetime import datetime
import dropbox
import requests
from dotenv import load_dotenv
load_dotenv()



from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DROPBOX_APP_KEY = os.environ.get('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
DROPBOX_REFRESH_TOKEN = os.environ.get('DROPBOX_REFRESH_TOKEN')

def GET_ACCESS_TOKEN():
    response = requests.post("https://api.dropbox.com/oauth2/token", data={
        "refresh_token": DROPBOX_REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "client_id": DROPBOX_APP_KEY,
        "client_secret": DROPBOX_APP_SECRET
    })
    return response.json()['access_token']


DROPBOX_ACCESS_TOKEN = GET_ACCESS_TOKEN()


@shared_task
def backup_postgres_and_upload(database_name, user, password, host, port, backup_dir):
    # Step 1: Perform the database backup
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = f"./database/{database_name}_backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_file)

    dump_cmd = f"PGPASSWORD={password} pg_dump -U {user} -h {host} -p {port} {database_name} > {backup_path}"
    subprocess.run(dump_cmd, shell=True, check=True)

    # Step 2: Upload the backup to Dropbox
    upload_to_dropbox(backup_path)

    # Optional: Remove the local backup file after upload
    os.remove(backup_path)

def upload_to_dropbox(file_path):
    # Create a Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    # Upload the backup file to Dropbox
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), f"/{os.path.basename(file_path)}")

    print(f"Backup uploaded to Dropbox: {file_path}")

