from django.urls import path
from users import views

app_name = 'users'

urlpatterns=[
    path('',views.profiles,name='all-profile'),
    path('single-profile/<str:pk>/',views.profile,name='single-profile'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('register/',views.registeruser,name='register'),
    path('account/',views.useraccount,name='account'),
    path('editprofile/',views.editprofile,name='editprofile'),

    path('create-skill/',views.createskill,name='create-skill'),
    path('update-skill/<str:pk>/',views.updateskill,name='update-skill'),
    path('delete-skill/<str:pk>/',views.deleteskill,name='delete-skill'),

    path('inbox/',views.inbox,name='inbox'),
    path('view-message/<str:pk>/',views.viewmessage,name='view-message'),
    path('create-message/<str:pk>/',views.createmessage,name='create-message')

]