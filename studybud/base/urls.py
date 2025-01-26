from django.urls import path
from base import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('register/',views.userregistration,name='register'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.create_room,name="create-room"),
    path('update-room/<str:pk>/',views.update_room,name="update-room"),
    path('delete-room/<str:pk>/',views.delete_room,name="delete-room"),
    path('delete-message/<str:pk>/',views.delete_message,name="delete-message"),
    path('profile/<str:pk>/',views.user_profile,name="user-profile"),
    path('update-user',views.UpdateUser,name="update-user"),
    path('topics',views.topicsPage,name="topics"),
    path('activity',views.activityPage,name="activity"),
]