from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'Solana/index.html')

def dashboard(request):
    if not request.session.get('is_authenticated'):
        return redirect('index')
    return render(request, 'Solana/dashboard.html')

def news(request):
    return render(request, 'Solana/news.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'Andreas' and password == 'GoodPassw0rd123':
            request.session['is_authenticated'] = True
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('index')
    return render(request, 'Solana/index.html')