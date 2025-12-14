from django.urls import path
from .clientnotes_views import (
    ClientNotesListCreateView,
    ClientNotesDetailView,
    client_notes_by_client
)

urlpatterns = [
    # ClientNotes CRUD
    path('', ClientNotesListCreateView.as_view(), name='clientnotes-list-create'),
    path('<int:pk>/', ClientNotesDetailView.as_view(), name='clientnotes-detail'),
    
    # Mijoz uchun ClientNotes
    path('client/<int:client_id>/', client_notes_by_client, name='clientnotes-by-client'),
]
