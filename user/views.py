from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

#signup用
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER","/"))
            #直前に使っていたページに戻る
    else:
        form = CustomUserCreationForm()
        
    return render(request,"user/signup.html", {"form": form})

@login_required
def user_info(request):
    user = request.user
    return render(request, "user/user_info.html", {"user":user})

@login_required
def user_delete(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request,"アカウントが削除されました。")
        return redirect("calculate")
    return render(request,"user/delete.html")