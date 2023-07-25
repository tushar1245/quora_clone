
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



from quora_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    # path('', views.base, name='base'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'home'), name='logout'),
    path('post_question/', views.post_question, name='post_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/post_answer/', views.post_answer, name='post_answer'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    
]

