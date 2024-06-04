from django.urls import path

from .views import *
urlpatterns=[
  path('',HomeView.as_view(),name='home'),
  path('item/<int:pk>/',ItemView.as_view(),name='item'),
  path('cart/<int:pk>/',CartView.as_view(),name='cart'),
  path('delete_cart_item/<int:pk>/',DeleteCartItemView.as_view(),name='delete_cart_item'),
  path('order/',OrderView.as_view(),name='order'),
  path('success/',SuccessView.as_view(),name='success'),
  path('index/', IndexView.as_view(), name='index'),
  path('upload_receipts/', UploadReceiptsView.as_view(), name='upload_receipts'),
  path('edit_receipts/', EditReceiptsView.as_view(), name='edit_receipts'),
  path('confirm_receipts/', ConfirmReceiptsView.as_view(), name='confirm_receipts'),
  path('save_to_csv/', SaveToCSVView.as_view(), name='save_to_csv'),
  path('save_complete/', SaveCompleteView.as_view(), name='save_complete'),
  # Reactを導入したテスト用ページ
  path('react/', render_react_view, name='react'),
]
