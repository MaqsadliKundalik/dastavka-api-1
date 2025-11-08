from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # User CRUD operatsiyalari
    path('', views.UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Authentication endpointlari
    path('register/', views.user_registration, name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    
    # Profile endpointlari
    path('profile/', views.user_profile, name='user-profile'),
]