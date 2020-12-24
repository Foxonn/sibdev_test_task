from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path(
        'upload/',
        views.UploadFileViewSet.as_view(),
        name='upload_file',
    ),
    path(
        'five_best_clients/',
        cache_page(
            60 * 60 * 24,
        )(
            views.ListDealsView.as_view()
        ),
        name='get_five_best_clients',
    ),
]
