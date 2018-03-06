from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import login, authenticate
from .forms import LoginForm, SignUpForm

# Create your views here.


def library(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = LoginForm()
    return render(request, 'library/libsystem.html', {'form': form})


def logined_library(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = LoginForm()
    return render(request, 'library/logined_libsystem.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = SignUpForm()
    return render(request, 'users/templates/library/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = LoginForm()
    return render(request, 'users/templates/library/login.html', {'form': form})

