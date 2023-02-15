from django import forms
from allauth.account.forms import SignupForm

#djangoのSignupFormは、adminで作るユーザー登録がadminによらずできるようになるライブラリ

#forms.pyは、html内の記述がPOSTで送られた際に、データベースに保存する為の設定を記述する場所。
#djangoのformsというライブラリのおかげです。

class ProfileForm(forms.Form):
    first_name = forms.CharField(label="姓", max_length=150)
    last_name = forms.CharField(label="名", max_length=150)
    description = forms.CharField(label="自己紹介", widget=forms.Textarea, max_length=150, required=False)# required=Falseにすることで、データが無い場合にも受け入れる。
    image = forms.ImageField(required=False,)


class SignupUserForm(SignupForm):#allauthのサインアップ機能を継承する。
    first_name = forms.CharField(max_length=30,label="姓")
    last_name = forms.CharField(max_length=30,label="名")
    #サインアップ時に所属など追加したい項目があれば、ここに追加する。

    def save(self,request):#サインアップボタンがクリックされた時の動作を下記で記載している。
        user = super(SignupUserForm,self).save(request)
        user.first_name = self.cleaned_data["first_name"]#上記のSignupUserFormで設定した内容を登録する記述である。
        user.last_name = self.cleaned_data["last_name"]
        user.save()#上記の設定した内容を保存する記述である。
        return user
