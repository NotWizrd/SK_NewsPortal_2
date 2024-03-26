from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostSearch, NewCreate, NewUpdate, NewDelete, subscriptions

urlpatterns = [
   # Path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('post/', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('post/search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewDelete.as_view(), name='news_delete'),
   path('articles/create/', NewCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', NewUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', NewDelete.as_view(), name='articles_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]