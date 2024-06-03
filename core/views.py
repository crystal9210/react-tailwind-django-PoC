from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView,DetailView,ListView
from django.views.generic.base import TemplateView, View #RedirectView
from django.shortcuts import render # to import React
from os import walk
import json
import stripe

from work_sample1.settings import STATIC_ROOT

from .forms import SearchForm
from .models import Item,CartItem, Order
# Create your views here.
stripe.api_key=settings.STRIPE_SECRET_KEY
User=get_user_model()

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user=self.request.user
        return (user.id==self.kwargs['pk']) or (user.is_superuser)# urlのpkは辞書型オブジェクトself.kwagsから取得可能


class HomeView(ListView):
    template_name = "core/home.html"
    model=Item
    paginate_by=4
    # 下の関数をオーバーライドすることでcontextにformを追加、テンプレ上で{{form}}利用可に
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=SearchForm
        return context

    def get_queryset(self):
        items=super().get_queryset()
        q_category=self.request.GET.get('category') # 辞書[キー]だと対象が存在しないときエラーが出るので、get(キー)でエラー回避
        if q_category is not None:
            items=items.filter(category=q_category)
        return items


class ItemView(DetailView):
    template_name = "core/item.html"
    model=Item
    def get_success_url(self):
        user_pk=self.request.user.id
        return reverse_lazy('cart',kwargs={'pk':user_pk})

    def post(self, *args, **kwargs):
        item_pk=self.request.POST.get('item_pk')
        quantity=self.request.POST.get('quantity')
        item=Item.objects.get(id=item_pk)
        cart_item=CartItem(item=item,quantity=quantity)
        user=self.request.user
        user.cart.add_cart_item(cart_item)
        return redirect(self.get_success_url())

class CartView(LoginRequiredMixin,OnlyYouMixin, DetailView):
    template_name = "core/cart.html"
    model=User
    context_object_name='cart'

    def get_object(self,queryset=None):
        user=super().get_object(queryset)
        return user.cart

class OrderView(View):
    def post(self,*args,**kwargs):
        """
        '購入へ進む'ボタンが押された時(=POSTリクエストが送信された時)
        Orderオブジェクトを作ると同時にユーザーのカートを空にします。
        [手順]
        1. Orderオブジェクトを作成
        2. カートの中身(cart_items)をOrderオブジェクトのorder_itemsにコピー
        3. カートの中身をリセット
        4. 決済ページにリダイレクト
        """
        order_user=self.request.user
        order_cart=order_user.cart
        order_obj=Order.objects.create(
            user=order_user,
            order_price=order_cart.total_price,
        )
        for cart_item in order_cart.cart_items.all():
            order_obj.order_items.add(cart_item)
        order_cart.cart_items.clear()

        """
        --------------------------------------------------------------
        2. Stripe決済処理
        --------------------------------------------------------------

        ユーザーをStripeの決済ページにリダイレクトさせます。
        [手順]
        2-1. line_items(購入情報のリスト)を作成
        2-2. checkout_sessionを作成
        2-3. 決済ページにリダイレクト
        """
        # 2-1. line_items(購入情報のリスト)を作成
        line_items = []
        for order_item in order_obj.order_items.all():
            line_item = {
                'price_data': {
                    'currency': 'jpy',
                    'unit_amount': order_item.item.price,
                    'product_data': {
                        'name': order_item.item.name,
                    }
                },
                'quantity': order_item.quantity,
            }
            line_items.append(line_item)
        # 2-2. checkout_sessionを作成
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                phone_number_collection={'enabled': False}, # 任意
                shipping_address_collection={'allowed_countries': []}, # 任意
                billing_address_collection='auto',  # 請求先住所の収集方法を自動に設定する
                success_url=settings.MYSITE_DOMAIN + '/success/',
            )
        except Exception as e:
            # エラーメッセージを適切なHTTPレスポンスとして返す
            return HttpResponse(str(e), status=500)

        # 正常な処理の場合、決済ページにリダイレクト
        return HttpResponseRedirect(checkout_session.url)

class DeleteCartItemView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    model = User

    def get_object(self, queryset=None):
        """
        デフォルトでDeleteViewが持っているget_objectメソッドを編集します。
        modelにユーザーモデルを指定しているので、このままでは削除対象となる
        オブジェクトはユーザーになります。
        ユーザーではなく、カートに入っている"特定のカートアイテム"を削除対象
        とするよう、以下の通りオーバーライドします。
        [手順]
        1. formからカートアイテムのpkを取得
        2. カートの中から、取得したpkと一致するカートアイテムを取得
        """
        user = super().get_object(queryset)
        # 1. formからカートアイテムのpkを取得
        cart_item_pk = int(self.request.POST['cart_item_pk'])  # 文字列から整数型に変換
        # 2. カートの中から、取得したpkと一致するカートアイテムを取得
        cart_item = user.cart.cart_items.get(id=cart_item_pk)
        return cart_item

    def get_success_url(self):
        """
        ユーザー専用のカートページURL(/cart/user_pk/)を取得するメソッドです。
        """
        user_pk = self.request.user.id
        return reverse_lazy('cart', kwargs={'pk': user_pk}) # kwargsの部分は args=(user_pk,) としてもOK


class SuccessView(TemplateView):
    template_name = "core/success.html"

class IndexView(TemplateView):
    template_name="core/index.html"

class UploadReceiptsView(TemplateView):
    template_name = "core/upload_receipts.html"

class EditReceiptsView(TemplateView):
    template_name = "core/edit_receipts.html"

class SaveCompleteView(TemplateView):
    template_name = "core/save_complete.html"



def render_react_view(request):
    onlyfiles = []
    for root, dirs, files in walk(STATIC_ROOT):
        for d in dirs:
            onlyfiles.append(root  + '/'+d)
        for f in files:
            onlyfiles.append(root  + '/'+f)
    return HttpResponse(json.dumps(onlyfiles),content_type="application/json")
