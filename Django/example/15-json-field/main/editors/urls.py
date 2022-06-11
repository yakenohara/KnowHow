from django.urls import path

from . import views

app_name = 'editors'
urlpatterns = [
    path('create/', views.EditorCreate.as_view(), name = 'create'),
    path('', views.EditorsList.as_view(), name = 'list'), # Read
    path('<int:pk>/update/', views.EditorUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', views.EditorDelete.as_view(), name = 'delete'),
    path('export_as_csv/', views.export_as_csv, name = 'export_as_csv'),
    path('import_from_csv/', views.import_from_csv, name = 'import_from_csv'),
]
