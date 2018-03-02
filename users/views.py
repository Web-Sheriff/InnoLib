from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

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
	return render(request, 'users/signup.html', {'form': form})


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
	return render(request, 'users/login.html', {'form': form})


