from django.shortcuts import render, redirect
from django.contrib import messages
import os
import hashlib

def index(request):

    trollflag = "Its not that easy buddy"
    heashed_trolledflag = hashlib.sha256(trollflag.encode()).hexdigest()
    response = render(request, 'Solana/index.html')
    response.set_cookie('Gemma-Lehre', f"{trollflag}" )

    return response 

def dashboard(request):
    # teamflag = os.environ.get('TEAMFLAG')
    teamflag = "teamflag"
    if not request.session.get('is_authenticated'):
        return redirect('index')
    
    else:
        challengeflag = "webchallenge1"
        
        combined_flag = challengeflag + teamflag
        
        hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()
        
        print(hashed_flag)
        response = render(request, 'Solana/dashboard.html')
        response.set_cookie('Flag', f"CHL{{{hashed_flag}}}", max_age=7*24*60*60)
        return response

def news(request):
    return render(request, 'Solana/news.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'Andreas' and password == 'GoodPassw0rd123':
            request.session['is_authenticated'] = True
            return redirect('dashboard')
        if username == 'Leon' and password =='Admin123':
            request.session['is_authenticated'] = True
            return redirect('wrong')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('index')
    return render(request, 'Solana/index.html')


def wrong(request):
    response = render(request, 'Solana/wrong.html')
    trollflag2 = "try /files"
    response.set_cookie('Flag', f"{trollflag2}" )
    return response

def files(request):
    response = render(request, 'Solana/files.html')
    return response