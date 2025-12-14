from django.urls import path
from .clientnotes_views import (
    get_client_notes,
    create_client_notes,
    update_client_notes,
    delete_client_notes
)

urlpatterns = [
    # ClientNotes CRUD by client_id
    path('<int:client_id>/', get_client_notes, name='clientnotes-get'),
    path('<int:client_id>/create/', create_client_notes, name='clientnotes-create'),
    path('<int:client_id>/update/', update_client_notes, name='clientnotes-update'),
    path('<int:client_id>/delete/', delete_client_notes, name='clientnotes-delete'),
]
