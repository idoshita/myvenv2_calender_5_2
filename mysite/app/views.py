from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# LoginRequiredMixinのライブラリを使うことで、ログアウト状態で、メインコンテンツに遷移した場合には、ログイン画面に遷移するようになる。

class IndexView(TemplateView):
    template_name = "app/index.html"