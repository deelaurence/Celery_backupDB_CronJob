from django.urls import path
from .views import *

urlpatterns=[
    path("quiz/", backup_quiz),
    path("blog/", backup_blog),
]