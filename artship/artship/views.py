# views.py
from django.shortcuts import redirect

def my_redirect_view(request):
    return redirect('/auction/') # Replace '/target-url/' with your desired URL