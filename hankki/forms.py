from django import forms
from django.forms import inlineformset_factory

from .models import HealthCategory, Allergy, LunchboxModel, OrderModel, OrderItemModel, IngredientsModel

class HealthCategoryForm(forms.ModelForm):
    class Meta:
        model = HealthCategory
        fields = ('name', 'description')



class IngredientsForm(forms.ModelForm):

    allergy = forms.MultipleChoiceField(
        required=False,
        choices=Allergy.get_choices(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.allergy:
            current_mask = self.instance.allergy
            selected_values = []
            for value, _ in Allergy.get_choices():
                if current_mask & value:
                    selected_values.append(str(value))
            self.initial['allergy'] = selected_values

    def clean_allergy(self):
        bitmask_value = 0
        for val_str in self.cleaned_data.get('allergy', []):
            bitmask_value |= int(val_str)
        return bitmask_value

    class Meta:
        model = IngredientsModel
        fields = ('name', 'allergy')


class LunchboxForm(forms.ModelForm):
    class Meta:
        model = LunchboxModel
        fields = [
            'name',
            'description',
            'image',
            'food_category',
            'health_category',
            'ingredient',
            'price',
            'discount_price',
            'stock',
        ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'health_category': forms.CheckboxSelectMultiple,
            'ingredient': forms.CheckboxSelectMultiple,
        }
        labels = {
            'name': '도시락 상품명',
            'description': '상세 설명',
            'image': '도시락 이미지',
            'food_category': '음식 종류',
            'health_category': '건강 카테고리',
            'ingredient': '포함 재료',
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
            'pickup_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mh-input',}),
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