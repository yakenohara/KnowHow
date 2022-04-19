from django.urls import path
from django.views.decorators.http import require_http_methods

import editors.views
import authors.views

app_name = 'apiv1'

urlpatterns = [
    path('editors/create/', require_http_methods(['POST'])(editors.views.EditorCreateAPIView.as_view()), name = 'editor_create'),
    path('editors.json/', require_http_methods(['HEAD', 'GET'])(editors.views.EditorListAPIView.as_view()), name = 'editors_list'),
    path('editors/update/', require_http_methods(['POST'])(editors.views.EditorUpdateAPIView.as_view()), name = 'editor_update'),
    path('editors/<int:pk>/delete/', require_http_methods(['DELETE'])(editors.views.EditorDeleteAPIView.as_view()), name = 'editor_delete'),
    path('authors/create/', require_http_methods(['POST'])(authors.views.AuthorCreateAPIView.as_view()), name = 'author_create'),
    path('authors.json/', require_http_methods(['HEAD', 'GET'])(authors.views.AuthorListAPIView.as_view()), name = 'authors_list'),
    path('authors/update/', require_http_methods(['POST'])(authors.views.AuthorUpdateAPIView.as_view()), name = 'author_update'),
    path('authors/<int:pk>/delete/', require_http_methods(['DELETE'])(authors.views.AuthorDeleteAPIView.as_view()), name = 'author_delete'),
]
