from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    path('create/', views.BookCreate.as_view(), name = 'create'),
    path('', views.Index.as_view(), name = 'index'),
    path('<int:pk>/update/', views.BookUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', views.BookDelete.as_view(), name = 'delete'),
    path('export_as_csv/', views.export_as_csv, name = 'export_as_csv'),
    path('import_from_csv/', views.import_from_csv, name = 'import_from_csv'),
]
