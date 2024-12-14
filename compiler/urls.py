from django.urls import path
from . import views
 
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    ## test endpoints
    path('', views.Welcome, name='root'),
    path('users/', views.getUsers, name='users'),
    path('jwtdata/', views.decodeJWT, name='getJWTdata'),
]