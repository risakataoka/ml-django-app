from django.urls import path
from . import views

from django.contrib import admin  # 追加
from django.views.generic import TemplateView  # 追加

app_name = 'machine'
urlpatterns = [
    path('', TemplateView.as_view(template_name='machine/index.html'), name='index'),
    path('upload/', views.upload, name='upload'),
]
