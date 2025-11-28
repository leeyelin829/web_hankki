from django.shortcuts import render


def lunch_detail(request):
    return render(request, 'hankki/lunch_detail.html')


def lunch_reserve(request):
    # 🔴 TODO: 백엔드 연동 필요
    # context = {
    #     'lunch': {
    #         'price': lunch.price,
    #         'stock': lunch.stock,
    #     },
    #     'user': {
    #         'balance': request.user.balance,
    #     }
    # }
    return render(request, 'hankki/lunch_reserve.html')


def lunch_complete(request):
    # reserve에서 전달받은 데이터 처리
    hour = request.GET.get('hour', '')
    minute = request.GET.get('minute', '')
    pickup_place = request.GET.get('pickup_place', '')
    quantity = request.GET.get('quantity', '0')
    total_price = request.GET.get('total_price', '0')

    # 픽업 장소 코드 → 한글 이름 변환
    place_map = {
        'hall': '학생회관 픽업존',
        'plaza': '연세플라자 픽업존'
    }
    pickup_place_name = place_map.get(pickup_place, '선택된 장소 없음')

    # 금액 포맷팅 (천 단위 콤마)
    try:
        total_price_formatted = f'{int(total_price):,}'
    except:
        total_price_formatted = '0'

    # context로 템플릿에 데이터 전달
    context = {
        'lunch': {
            'name': '도시락 패키지 이름',  # 🔴 TODO: DB에서 가져오기
        },
        'hour': hour,
        'minute': minute,
        'pickup_place_name': pickup_place_name,
        'quantity': quantity,
        'total_price': total_price_formatted,
    }

    return render(request, 'hankki/lunch_complete.html', context)


def charge(request):
    return render(request, 'hankki/charge.html')