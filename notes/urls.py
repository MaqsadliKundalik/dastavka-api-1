from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('<int:pk>/', views.NoteRetrieveUpdateDestroyView.as_view(), name='note-retrieve-update-destroy'),
]