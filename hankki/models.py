from enum import Enum, IntEnum
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


class Allergy(IntEnum):
    EGG = 1 << 0        # 난류
    MILK = 1 << 1       # 우유
    BUCKWHEAT = 1 << 2  # 메밀
    PEANUT = 1 << 3     # 땅콩
    SOY = 1 << 4        # 대두
    WHEAT = 1 << 5      # 밀
    MACKEREL = 1 << 6   # 고등어
    CRAB = 1 << 7       # 게
    SHRIMP = 1 << 8     # 새우
    PORK = 1 << 9       # 돼지고기
    PEACH = 1 << 10     # 복숭아
    TOMATO = 1 << 11    # 토마토
    SULFITES = 1 << 12  # 아황산염
    WALNUT = 1 << 13    # 호두
    CHICKEN = 1 << 14   # 닭고기
    BEEF = 1 << 15      # 쇠고기
    SQUID = 1 << 16     # 오징어
    SHELLFISH = 1 << 17 # 조개류
    PINE_NUT = 1 << 18  # 잣

    @classmethod
    def get_choices(cls):
        return [
            (cls.EGG.value, '난류'),
            (cls.MILK.value, '우유'),
            (cls.BUCKWHEAT.value, '메밀'),
            (cls.PEANUT.value, '땅콩'),
            (cls.SOY.value, '대두'),
            (cls.WHEAT.value, '밀'),
            (cls.MACKEREL.value, '고등어'),
            (cls.CRAB.value, '게'),
            (cls.SHRIMP.value, '새우'),
            (cls.PORK.value, '돼지고기'),
            (cls.PEACH.value, '복숭아'),
            (cls.TOMATO.value, '토마토'),
            (cls.SULFITES.value, '아황산염'),
            (cls.WALNUT.value, '호두'),
            (cls.CHICKEN.value, '닭고기'),
            (cls.BEEF.value, '쇠고기'),
            (cls.SQUID.value, '오징어'),
            (cls.SHELLFISH.value, '조개류'),
            (cls.PINE_NUT.value, '잣'),
        ]




class HealthCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)     # 카테고리 이름
    description = models.TextField(blank=True)              # 카테고리 설명

    def __str__(self):
        return self.name



class IngredientsModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    allergy = models.IntegerField()

    def __str__(self):
        return self.name

    # 비트마스킹으로 알레르기 정보 저장
    # ① 난류, ② 우유, ③ 메밀, ④ 땅콩, ⑤ 대두, ⑥ 밀, ⑦ 고등어, ⑧ 게, ⑨ 새우, ⑩ 돼지고기
    # ⑪ 복숭아, ⑫ 토마토, ⑬ 아황산염, ⑭ 호두, ⑮ 닭고기, ⑯ 쇠고기, ⑰ 오징어, ⑱ 조개류, ⑲ 잣



class LunchboxModel(models.Model):
    # 도시락 정보
    name = models.CharField(max_length=127)                                                             # 도시락 이름
    description = models.TextField()                                                                    # 도시락 설명
    image = models.ImageField(upload_to='lunchbox/', blank=True, null=True)                             # 도시락 이미지

    # 재료 목록
    ingredient = models.ManyToManyField(IngredientsModel, blank=True, null=True)                              # 재료

    # 도시락 카테고리
    food_category = models.CharField(choices=FoodCategory.choices(), max_length=20, blank=True)         # 음식 카테고리
    health_category = models.ManyToManyField(HealthCategory, related_name='lunchbox', blank=True)       # 건강 관련 카테고리

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