import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, DeleteView

from .forms import TokenEditForm
from .models import TokenForRESTAPI

# Create your views here.

class AccountCreateView(CreateView):
    model = User
    template_name = 'accounts/form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:list')

class AccountsListView(ListView):
    model = User
    
    queryset = User.objects.prefetch_related('auth_token')
    #
    # note1
    # `queryset`
    # View 関数がテンプレートに返すオブジェクトリスト。指定されていない場合は、`model = ` に指定したモデルの `.objects.a()` が指定される。
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model
    #
    # note2
    # `.prefetch_related('auth_token')`
    # django-rest-framework が提供する rest_framework.authtoken.models.Token モデルが User を外部キーとして参照している。  
    # その為、User から Token モデルを参照(逆参照)するため `prefetch_related` で取得している。  
    # https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/models.py



    template_name = 'accounts/list.html'
    success_url = reverse_lazy('accounts:list')

class AccountDelete(DeleteView):
    model = User
    success_url = reverse_lazy('accounts:list')

def createToken(request, pk):

    obj_user = get_object_or_404(User, id = pk)
    # note
    # `get_object_or_404`
    # オブジェクトを検索し、存在しない場合は `Http404` を Raise する
    # https://docs.djangoproject.com/ja/2.2/topics/http/shortcuts/#django.shortcuts.get_object_or_404
    
    if request.method == 'POST':
        
        obj_form = TokenEditForm(request.POST)
        
        if obj_form.is_valid():

            TokenForRESTAPI.objects.filter(user = obj_user).delete() # 既存のトークンを削除

            obj_token = obj_form.save(commit = False) # データベースに保存する前のモデルインスタンスを取得

            # 有効期限の設定
            if obj_token.expiration == TokenForRESTAPI.Expiration.ONE_WEEK:
                obj_token.expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
            elif obj_token.expiration == TokenForRESTAPI.Expiration.ONE_MONTH:
                obj_token.expired_date = make_aware(datetime.datetime.now()) + relativedelta(months = 1) # 1 ヶ月加算
            elif obj_token.expiration == TokenForRESTAPI.Expiration.THREE_MONTHS:
                obj_token.expired_date = make_aware(datetime.datetime.now()) + relativedelta(months = 3) # 3 ヶ月加算
            else:
                obj_token.expired_date = None

            obj_token.user = obj_user # ユーザーの設定

            obj_token.save()

            return JsonResponse({'token': obj_token.key})

    else: # request method が GET の場合
        obj_form = TokenEditForm()
    
    # form が invalid もしくは request method が GET の場合
    return render(request, "accounts/form_token.html", {'form': obj_form})

def deleteToken(request, pk):

    obj_user = get_object_or_404(User, id = pk)

    TokenForRESTAPI.objects.filter(user = obj_user).delete()

    return redirect('accounts:list')
