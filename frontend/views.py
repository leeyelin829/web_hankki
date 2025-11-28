from django.shortcuts import render

def order(request):
    meals = [
        {'name': '샘플 도시락1', 'price': 5000, 'image': '/static/frontend/img/sample1.jpg'},
        {'name': '샘플 도시락2', 'price': 6000, 'image': '/static/frontend/img/sample2.jpg'},
    ]

    return render(request, 'frontend/order.html', {'meals': meals})
