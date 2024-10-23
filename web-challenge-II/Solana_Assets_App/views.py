from django.shortcuts import render, redirect
from django.contrib import messages
import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def index(request):
    trollflag = "Its not that easy buddy"
    heashed_trolledflag = hashlib.sha256(trollflag.encode()).hexdigest()
    response = render(request, 'Solana/index.html')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    response.set_cookie('Gemma-Lehre', f"{trollflag}" )

    return response 

def dashboard(request):
    #! This is the flag that you need to get from the environment variables
    # teamflag = os.environ.get('TEAMFLAG')
    teamflag = "teamflag"
    if not request.session.get('is_authenticated'):
        return redirect('index')
    
    else:
        challengeflag = "nkN7FPpuB#"
        combined_flag = challengeflag + teamflag
        hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()

        logging.info(f'Hashed Flag: {hashed_flag}')

        response = render(request, 'Solana/dashboard.html')
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)        
        response.set_cookie('Flag', f"TH{{{hashed_flag}}}", max_age=7*24*60*60)

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
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    response.set_cookie('Flag', f"{trollflag2}" )
    return response

def files(request):
    response = render(request, 'Solana/files.html')
    return response