from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.Welcome, name='root'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login')
]