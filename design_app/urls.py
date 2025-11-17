from django.urls import path
from . import views

app_name = 'design_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('create-request/', views.create_request_view, name='create_request'),
    path('delete-request/<int:request_id>/', views.delete_request_view, name='delete_request'),
    path('manager/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/requests/', views.admin_requests, name='admin_requests'),
    path('manager/change-status/<int:request_id>/', views.change_request_status, name='change_status'),
    path('manager/categories/', views.manage_categories, name='manage_categories'),
]