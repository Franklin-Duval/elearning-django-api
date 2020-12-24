from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'course', views.CourseViewSet)
routers.register(r'classe', views.ClasseViewSet)
routers.register(r'subject', views.SubjectViewSet)
routers.register(r'user', views.UserViewSet)
routers.register(r'exam', views.ExamViewSet)
routers.register(r'comment', views.CommentViewSet)
routers.register(r'inscription', views.InscriptionViewSet)


urlpatterns = [
    path('', include(routers.urls))
]