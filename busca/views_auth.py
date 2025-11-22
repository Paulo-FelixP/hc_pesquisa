from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_manual(request):
    logout(request)
    return redirect('/')
