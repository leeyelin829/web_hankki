from django import forms
from django.forms import inlineformset_factory

from .models import HealthCategory, LunchboxModel, OrderModel, OrderItemModel

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




class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = [
            'pickup_date_time',
            'is_delivery',
            'delivery_address'
        ]
        widgets = {
            'pickup_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        is_delivery = cleaned_data.get('is_delivery')
        delivery_address = cleaned_data.get('delivery_address')
        if is_delivery and not delivery_address:
            self.add_error('delivery_address', "배달을 선택하면 주소는 필수입니다.")

        return cleaned_data


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItemModel
        fields = [
            'lunchbox',
            'quantity',
            'price'
        ]
        widgets = {
            'price': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lunchbox'].queryset = LunchboxModel.objects.all()


OrderItemFormSet = inlineformset_factory(
    OrderModel,
    OrderItemModel,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)