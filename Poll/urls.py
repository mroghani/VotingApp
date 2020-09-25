from django.urls import path

from . import views


urlpatterns = [
    path('<str:token>', views.index, name='index'),
]