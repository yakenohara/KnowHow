"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # <- `include` を追加

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # note
    # 第1引数には ``<`~python.exe manage.py startapp xxx` で作成したアプリ名>/`` を指定
    # 第2引数には ``include('<`~python.exe manage.py startapp xxx` で作成したアプリ名>.urls')`` を指定
    path('editors/', include('editors.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('index.urls')),
    # URL で API のメジャーバージョンが指定できるように、`v1/` を URL に追加
    path('api/v1/', include('common.apiv1_urls')),
    
    # Open API 準拠の API ドキュメント生成の為の定義
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html#take-it-for-a-spin
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
