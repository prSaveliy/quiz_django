from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('quizzes/create/', views.quiz_create, name='quiz_create'),
    path('my_quizzes/', views.user_quizzes, name='user_quizzes'),
    path('quizzes/<int:quiz_id>/confirm_delete/', views.quiz_confirm_delete, name='quiz_confirm_delete'),
    path('quizzes/<int:quiz_id>/delete/', views.quiz_delete, name='quiz_delete'),
    path('my_results/', views.user_quizzes_results, name='user_quizzes_results'),
]