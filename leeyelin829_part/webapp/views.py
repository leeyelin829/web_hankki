# webapp/views.py

from django.shortcuts import render

def index(request):
    context = {
        'title': '메인 페이지',
        'message': 'Django 첫 웹페이지다!'
    }
    return render(request, 'webapp/index.html', context)

def service(request):
    context = {
        'title': '서비스 소개',
        'message': '여기에 서비스 설명을 적을 수 있다.'
    }
    return render(request, 'webapp/service.html', context)
