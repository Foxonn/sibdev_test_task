from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path(
        'upload/',
        views.UploadFileAPIView.as_view(),
        name='upload_file',
    ),
    path(
        'five_best_clients/',
        views.ListDealsView.as_view(),
        name='get_five_best_clients',
    ),
]
