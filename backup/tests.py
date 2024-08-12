# from django.test import TestCase
# import requests
# # Create your tests here.
# import dropbox

# def DROPBOX_ACCESS_TOKEN():
#     response = requests.post("https://api.dropbox.com/oauth2/token", data={
#         "refresh_token": DROPBOX_REFRESH_TOKEN,
#         "grant_type": "refresh_token",
#         "client_id": DROPBOX_APP_KEY,
#         "client_secret": DROPBOX_APP_SECRET
#     })
#     return response.json()['access_token']


# DROPBOX_NEW_TOKEN=DROPBOX_ACCESS_TOKEN()


# # Path to the file you want to upload
# file_to_upload = 'test_file.txt'

# # Create a sample file to upload (if it doesn't exist)
# with open(file_to_upload, 'w') as f:
#     f.write("This is a test file for Dropbox upload.\n")

# # Initialize Dropbox client
# dbx = dropbox.Dropbox(DROPBOX_NEW_TOKEN)

# try:
#     # Upload the file to Dropbox
#     with open(file_to_upload, 'rb') as f:
#         dbx.files_upload(f.read(), f"/{file_to_upload}")

#     print(f"File '{file_to_upload}' uploaded successfully to Dropbox!")
# except dropbox.exceptions.AuthError as err:
#     print(f"ERROR: Authentication failed: {err}")
# except dropbox.exceptions.ApiError as err:
#     print(f"ERROR: API error: {err}")
# except Exception as e:
#     print(f"ERROR: An unexpected error occurred: {e}")
