from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import SignupForm
# Create your views here.
User=get_user_model()
class SignupView(CreateView):
    template_name = "registration/signup.html" # ユーザ登録フォームを表示させるためのビュークラス
    model=User # ビューで作成されるオブジェクトのモデルを指定
    form_class=SignupForm # ユーザ登録に使用するフォームクラスを指定、このフォームはフォームフィールド・バリデーションの定義を含んでいる
    success_url=reverse_lazy('signup_done') # ユーザ登録が完了した後にリダイレクトするurl


class SignupDoneView(TemplateView):
    template_name = "registration/signup_done.html"
