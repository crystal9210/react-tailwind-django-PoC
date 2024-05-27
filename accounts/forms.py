from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.models import Cart


User=get_user_model()

class SignupForm(UserCreationForm):
  def __init__(self,*args, **kwargs):
    super().__init__(*args,**kwargs)
    self.fields["username"].widget.attrs.update({"class":"form-control"})
    self.fields["password1"].widget.attrs.update({"class":"form-control"})
    self.fields["password2"].widget.attrs.update({"class":"form-control"})
  def save(self):
    """
        ユーザー作成と同時にそのユーザーにカートを持たせるメソッドです。
        [手順]
        1. フォーム入力情報に基づきユーザーオブジェクトを作成（まだデータベースに保存しない）
        2. 新しいカートオブジェクトを作り、ユーザーのカートフィールドに代入
        3. ユーザーオブジェクトをデータベースに保存
        """
    user = super().save(commit=False)   # 親クラスが持つデフォルトのsaveメソッドでユーザーオブジェクトを作成
                                            # (commit=Falseとすることで、この時点ではデータベースに保存されない)
    user.cart = Cart.objects.create()
    user.save() # ここでデータベースに保存
    return user
  class Meta:
    model=User
    fields=('username',) # pw以外で表示したい項目を書く、pwは書かなくても自動で表示される
