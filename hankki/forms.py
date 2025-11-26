from django import forms

from .models import HealthCategory, LunchboxModel

class HealthCategoryForm(forms.ModelForm):
    class Meta:
        model = HealthCategory
        fields = ('name', 'description')


class LunchboxForm(forms.ModelForm):
    class Meta:
        model = LunchboxModel
        fields = [
            'name',
            'description',
            'food_category',
            'health_category',
            'price',
            'discount_price',
            'stock',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'health_category': forms.CheckboxSelectMultiple,
        }
        labels = {
            'name': '도시락 상품명',
            'description': '상세 설명',
            'food_category': '음식 종류',
            'health_category': '건강 카테고리',
            'price': '판매 가격',
            'discount_price': '할인 가격',
            'stock': '재고 수량',
        }


class SupplierPermissionRequestForm(forms.Form):
    agreement = forms.BooleanField(
        label='도시락 공급자 약관에 동의하며, 관련 책임 및 의무를 이해했습니다.',
        required=True,
        error_messages={'required': '약관에 동의하셔야 권한을 획득할 수 있습니다.'}
    )