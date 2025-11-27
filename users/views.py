from django.shortcuts import render, redirect
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

# ✅ 스플래시 화면
def splash(request):
    return render(request, 'splash.html')


# ✅ 온보딩 화면
def onboarding(request):
    return render(request, 'onboarding.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})