from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.urls import reverse
from . import views
app_name ='predict'
urlpatterns = [
    path('', views.Home, name='prediction_page'),
    path('results/', views.view_results, name='results'),
    path('delete/<int:id>', views.destroy),
]
# </int:id></int:id></int:id>