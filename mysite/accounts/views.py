from django.shortcuts import render, redirect
from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm,SignupUserForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin

# LoginRequiredMixinのライブラリを使うことで、ログアウト状態で、メインコンテンツに遷移した場合には、ログイン画面に遷移するようになる。


class ProfileView(LoginRequiredMixin, View):
    def get(self, request,*args,**kwargs):#GETに必要な記述
        user_data = CustomUser.objects.get(id=request.user.id) # データベースからカスタムユーザーを取得する。
        return render(request,"accounts/profile.html",{# この分により、GETで呼ばれた際に、profile.htmlを表示する。
        "user_data":user_data,
        })



class EditView(LoginRequiredMixin, View):
    def get(self, request,*args,**kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)# データベースからカスタムユーザーを取得する。
        form = ProfileForm(
            request.POST or None,# GETで呼び出した際には、Noneなので、単純なデータベースを表示する。POSTされた際にformを表示。
            initial={# initialは、インスタンスのフォーム初期化時に設定するものである。
                "first_name":user_data.first_name,
                "last_name":user_data.last_name,
                "description":user_data.description,
                "image":user_data.image,
            }
        )

        return render(request,"accounts/profile_edit.html",{
            "form":form,
        })


    def post(self, request,*args,**kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():# .is_validでformの内容をチェックする
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data["first_name"]#フォームされた時の処理なので、.cleaned_dataで、formで送られた情報を取得する。
            user_data.last_name = form.cleaned_data["last_name"]
            user_data.description = form.cleaned_data["description"]
            if request.FILES.get("image"):#もし画像が変更された場合は、
                user_data.image = request.FILES.get("image")
            user_data.save()#.cleaned_dataで変更になったデータをセーブ(保存)する。
            return redirect("profile")#セーブが完了したら、プロフィールに遷移します。

        return render(request,"accounts/profile.html",{
            "form":form,
        })


class LoginView(views.LoginView):#allauthのログインビューを継承する。これで簡単にログインが可能となる。
    template_name = "accounts/login.html"


class LogoutView(views.LogoutView):#allauthのログアウトビューを継承する。これで簡単にログインが可能となる。
    template_name = "accounts/logout.html"

    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated:#userのログイン状態を把握して、「もしログイン状態でポストされたなら」
            self.logout()#ログアウトする。
            return redirect("/")#ログアウトしたらトップページに遷移する。


class SignupView(views.SignupView):#allauthのサインアップビューを継承する。これで簡単にサインアップが可能となる。
    template_name = "accounts/signup.html"
    form_class = SignupUserForm #この記述により、オリジナルのフォームを利用する事ができるようになる。
