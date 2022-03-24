from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'todo-viewset', views.TodoViewSet, basename='todo')

urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('post_val', views.post_data, name='post_val'), # need to implement
    path('update_val', views.update_data, name='update_val'),
    # path('', views.index, name = 'mobileapp'),
    # path("about", views.about, name='about'),
    path('post_todo/', views.post_todo, name='post_todo'),
    path('get_todo/', views.get_todo, name='get_todo'),
    path('update_todo/', views.update_todo, name='update_todo'),
    path('todoview/', views.TodoView.as_view(), name='update_todo'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('items/', views.Items.as_view(), name='items'),
    
]

urlpatterns += router.urls