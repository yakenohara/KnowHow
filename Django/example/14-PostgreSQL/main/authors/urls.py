from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('create/', views.AuthorCreate.as_view(), name = 'create'),
    path('', views.AuthorsList.as_view(), name = 'list'), # Read
    path('<int:pk>/update/', views.AuthorUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'delete'),
    path('export_as_csv/', views.export_as_csv, name = 'export_as_csv'),
    path('import_from_csv/', views.import_from_csv, name = 'import_from_csv'),
]
