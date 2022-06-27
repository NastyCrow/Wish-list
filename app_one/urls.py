from django.urls import path
from . import views

urlpatterns =[
    path('',views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard',views.dashboard),
    path('wish_items/create',views.create_item),
    path('wish_items/<int:id>',views.show_item),
    path('add_item/<int:id>',views.add_item),
    path('delete_item/<int:id>',views.delete_item),
    path('remove_item/<int:id>',views.remove_item),
]