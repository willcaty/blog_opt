# -*- coding; utf-8 -*-

from django.urls import path

from . import views


urlpatterns = [
    path('index/', views.index),
    path('detail/<int:article_id>/', views.detail),
    path('comment/<int:article_id>/', views.add_comment),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view),
    path('register/', views.register_view, name='register'),
    path('search/', views.search_view, name='search'),
    path('add/', views.add_page, name='add'),
    path('add_article/', views.add_article, name='add')
]
