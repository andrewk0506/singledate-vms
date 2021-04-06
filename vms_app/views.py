from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, "index.html", {})

def preregister(request):
	return render(request, "preregister.html", {})

def check(request):
	return render(request, "check.html", {})

def signup(request):
	return render(request, "signup.html", {})

def verify(request):
	return render(request, "verify.html", {})
