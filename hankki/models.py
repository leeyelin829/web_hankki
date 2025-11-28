from enum import Enum
from django.db import models
from django.conf import settings


class FoodCategory(Enum):
    KOREAN = 'KOREAN'       # 한식
    JAPANESE = 'JAPANESE'   # 일식
    WESTERN = 'WESTERN'     # 양식
    SALAD = 'SALAD'         # 샐러드
    DIET = 'DIET'           # 다이어트식
    ETC = 'ETC'             # 기타

    @classmethod
    def choices(cls):
        return [
            (cls.KOREAN.value, '한식'),
            (cls.JAPANESE.value, '일식'),
            (cls.WESTERN.value, '양식'),
            (cls.SALAD.value, '샐러드'),
            (cls.DIET.value, '다이어트식'),
            (cls.ETC.value, '기타'),
        ]


class HealthCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)     # 카테고리 이름
    description = models.TextField(blank=True)              # 카테고리 설명

    def __str__(self):
        return self.name


class LunchboxModel(models.Model):
    # 도시락 정보
    name = models.CharField(max_length=127)                                                             # 도시락 이름
    description = models.TextField()                                                                    # 도시락 설명
    image = models.ImageField(upload_to='lunchbox/', blank=True, null=True)                             # 도시락 이미지

    # 도시락 카테고리
    food_category = models.CharField(choices=FoodCategory.choices(), max_length=20, blank=True)         # 음식 카테고리
    health_category = models.ManyToManyField('HealthCategory', related_name='lunchbox', blank=True)     # 건강 관련 카테고리

    # 가격 / 할인 가격 정보
    price = models.IntegerField()                                                                       # 가격
    discount_price = models.IntegerField(default=0)                                                     # 할인 금액

    # 공급 정보
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)                    # 공급자
    stock = models.IntegerField(default=0)                                                              # 재고

    # DB 등록 시간 정보
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("lunchbox_supplier", "도시락 판매자"),
        ]


class OrderStatus(Enum):
    PENDING = 'PENDING'             # 주문 대기
    PREPARING = 'PREPARING'         # 상품 준비 중

    READY_PICKUP = 'READY_PICKUP'   # 픽업 준비 완료
    IN_DELIVERY = 'IN_DELIVERY'     # 배달 중

    COMPLETED = 'COMPLETED'         # 완료
    CANCELLED = 'CANCELLED'         # 주문 취소

    @classmethod
    def choices(cls):
        return [
            (cls.PENDING.value, '주문 대기'),
            (cls.PREPARING.value, '상품 준비 중'),
            (cls.READY_PICKUP.value, '픽업 준비 완료'),
            (cls.IN_DELIVERY.value, '배송 중'),
            (cls.COMPLETED.value, '완료'),
            (cls.CANCELLED.value, '주문 취소'),
        ]


class OrderModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=OrderStatus.choices(), max_length=20, blank=True)

    # 주문 가격
    price = models.IntegerField()

    # 예약 시간 (null인 경우 일반 주문)
    pickup_date_time = models.DateTimeField(blank=True, null=True)

    # 배달 정보
    is_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)

    # DB 등록 시간 정보
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    lunchbox = models.ForeignKey(LunchboxModel, on_delete=models.SET_NULL, null=True)

    # 주문 가격 및 수량
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    # DB 등록 시간 정보
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)




class CartItemModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    lunchbox = models.ForeignKey(LunchboxModel, on_delete=models.CASCADE)

    # 수량
    quantity = models.IntegerField(default=1)

    # DB 등록 시간 정보
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)