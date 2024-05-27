from django.conf import settings
from django.db import models

"""
---------------------------
ユーザーモデルの読み込み方法３種
---------------------------

1. settingsファイルから取得
from django.conf import settings
User = settings.AUTH_USER_MODEL

2. get_user_modelで取得
from django.contrib.auth import get_user_model
User = get_user_model()

3. 直接インポートして取得
from accounts.models import CustomUser

"""
# Create your models here.
User=settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = '商品カテゴリ'
        verbose_name_plural = '商品カテゴリ'

    def __str__(self):
        return self.name

class Item(models.Model):
  name=models.CharField(max_length=100)
  price=models.PositiveBigIntegerField()
  description=models.TextField(blank=True,null=True)
  image=models.ImageField(upload_to='item_images/',blank=True,null=True)
  category=models.ForeignKey(to=Category,on_delete=models.SET_DEFAULT,default=1)

  class Meta:
    verbose_name='商品',
    verbose_name_plural='商品'

  def __str__(self):
    return self.name

class CartItem(models.Model):
  item=models.ForeignKey(to=Item,on_delete=models.CASCADE) # CASCADE:
  quantity=models.PositiveIntegerField(default=1)
  @property
  def total_price(self):
    return self.item.price*self.quantity

class Cart(models.Model):
  cart_items=models.ManyToManyField(to=CartItem,blank=True)

  def add_cart_item(self,new_cart_item):
    if new_cart_item in [cart_item.item for cart_item in self.cart_items.all()]:
      original_cart_item=self.cart_items.get(item_id=new_cart_item.item.id)
      original_cart_item.quantity+=new_cart_item.quantity
      original_cart_item.save()
    else:
      new_cart_item.save()
      self.cart_items.add(new_cart_item)
  @property
  def total_price(self):
    return sum([cart_item.total_price for cart_item in self.cart_items.all()])
# メモ：many to many fieldにおいてnull=Trueは無意味なので不要、書いた場合、null has no effect on many to many fieldという警告が出る

class Order(models.Model):
  user=models.ForeignKey(to=User, on_delete=models.CASCADE)
  order_items=models.ManyToManyField(to=CartItem,blank=True) # blankはなんの属性か
  order_price = models.PositiveIntegerField()
  ordered_date=models.DateTimeField(auto_now=True)
