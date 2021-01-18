from django.urls import path
from . import views


app_name = 'pic_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('edit/<int:pk>/', views.edit_picture, name='edit_picture'),
]
