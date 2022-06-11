from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', CreateView.as_view(
        template_name = 'accounts/form.html',
        form_class = UserCreationForm,
        success_url = '/',
    ), name='signup'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user = True,
        # note
        # ログインページにアクセスする認証済みユーザーが、ログインに成功したかのようにリダイレクトさせる。
        # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.redirect_authenticated_user
        
        template_name = 'accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('', views.AccountsListView.as_view(), name = 'list'), # Read
    path('<int:pk>/delete/', views.AccountDelete.as_view(), name = 'delete'),
    path('<int:pk>/token/create/', views.createToken, name = 'create_token'),
    path('<int:pk>/token/delete/', views.deleteToken, name = 'delete_token'),
]
