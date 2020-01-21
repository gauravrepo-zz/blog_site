from .views import create_blog_view, my_blogs_list_view, update_blog_view, detail_blog_view, delete_blog_view
from django.urls import path

urlpatterns = [
    path('create', create_blog_view, name="create_blog"),
    path('myblogs', my_blogs_list_view, name="my_blogs"),
    path('<slug>', detail_blog_view, name="detail_blog"),
    path('<slug>/update-blog', update_blog_view, name="update_blog"),
    path('<slug>/delete-blog', delete_blog_view, name="delete_blog"),

]
