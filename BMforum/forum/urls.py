#forum\urls.py
from django.urls import path #导入path函数
from . import views 	#从当前的目录下导入views模块

app_name = 'forum'
urlpatterns = [			#网址和处理函数的关系写在urlpatterns列表里面
    path('index/', views.IndexView.as_view(), name='index'),
    path('books_index/', views.BooksIndexView.as_view(), name='book_index'),	#第一个参数是网址，第二个参数是处理函数#第三个name 为传递的参数，这个参数的值作为处理函数index的别名（我也不太懂）
    path('movies_index/', views.MoviesIndexView.as_view(), name='movie_index'),
    #path('groups/', views.MoviesIndexView.as_view(), name='groups'),
    path('topic/', views.TopicIndexView.as_view(), name='topic_index'),
    path('books/<int:pk>/', views.PostDetailView.as_view(), name='book_detail'),
    path('movies/<int:pk>/', views.MoviePostDetailView.as_view(), name='movie_detail'),
    path('topics/<int:pk>/', views.TopicPostDetailView.as_view(), name='topic_detail'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    #path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    #path('search/', views.search, name='search'),
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]