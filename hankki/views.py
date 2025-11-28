import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.db import transaction
from django.urls import reverse_lazy

from .apps import HankkiConfig
from .models import HealthCategory, LunchboxModel, OrderStatus, OrderModel, OrderItemModel, CartItemModel
from .forms import HealthCategoryForm, LunchboxForm, SupplierPermissionRequestForm, OrderForm, OrderItemFormSet


logger = logging.getLogger(HankkiConfig.name)



# ================
#  HealthCategory
# ================

@user_passes_test(lambda user: user.is_authenticated and user.is_superuser, login_url='/auth/login/')
def write_health_category(request, id=None):
    if id:
        health_category = get_object_or_404(HealthCategory, id=id)
    else:
        health_category = None

    if request.method == 'POST':
        form = HealthCategoryForm(request.POST, instance=health_category)

        if form.is_valid():
            health_category = form.save()

            return redirect('/')
    else:
        form = HealthCategoryForm(instance=health_category)

    context = {'form': form}
    return render(request, 'health_category_form.html', context)



# ===========
#  Lunchbox
# ===========

@login_required
@permission_required('lunchbox_supplier', login_url=reverse_lazy('hankki:supplier'))
def write_lunchbox(request, id=None):
    if id:
        lunchbox = get_object_or_404(LunchboxModel, pk=id)
        if lunchbox.supplier != request.user:
            return redirect('/')
    else:
        lunchbox = None

    if request.method == 'POST':
        form = LunchboxForm(request.POST, request.FILES, instance=lunchbox)

        if form.is_valid():
            lunchbox = form.save(commit=False)
            if not lunchbox.supplier_id:
                lunchbox.supplier = request.user
            lunchbox.save()

            form.save_m2m()
            return redirect('/')
    else:
        form = LunchboxForm(instance=lunchbox)

    context = {'form': form}
    return render(request, 'lunchbox_form.html', context)


def delete_lunchbox(request, id):
    lunchbox = get_object_or_404(LunchboxModel, id=id)
    lunchbox.delete()
    return redirect('/')



# ===========
#  Order
# ===========

@login_required
def order(request, id=None):
    if id:
        order = get_object_or_404(OrderModel, id=id)
        if order.user != request.user:
            return redirect('/')
    else:
        order = None

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            if id:
                queryset = order.orderitemmodel_set.all()
            else:
                queryset = CartItemModel.objects.filter(user=request.user)
            if queryset.exists():
                with transaction.atomic():

                    order = form.save(commit=False)
                    order.user = request.user
                    order.status = OrderStatus.PENDING.value

                    price_sum = 0;
                    order_item_list = []
                    for item in queryset:
                        lunchbox = item.lunchbox
                        quantity = item.quantity
                        price_sum += (lunchbox.price - lunchbox.discount_price) * quantity

                    order.price = price_sum
                    order.save()

                    for item in queryset:
                        lunchbox = item.lunchbox
                        quantity = item.quantity
                        order_item = OrderItemModel(
                            order=order,
                            lunchbox=lunchbox,
                            quantity=quantity,
                            price=(lunchbox.price - lunchbox.discount_price) * quantity,
                        )
                        order_item.save()
                        item.delete()

                    return redirect('/')
    else:
        form = OrderForm(instance=order)

    if id:
        queryset = order.orderitemmodel_set.all()
        # queryset = [item.lunchbox for item in queryset]
        context = {'form': form, 'is_edit': True, 'queryset': queryset}
    else:
        queryset = CartItemModel.objects.filter(user=request.user).select_related('lunchbox')
        # queryset = [item.lunchbox for item in queryset]
        context = {'form': form, 'is_edit': False, 'queryset': queryset}
    return render(request, 'order_form.html', context)



# ===========
#  Cart
# ===========

def lunchbox_list(request):
    context = {'lunchboxes': LunchboxModel.objects.all()}
    return render(request, 'lunchbox_list.html', context)


@login_required
def cart(request, id, quantity=1):
    lunchbox = get_object_or_404(LunchboxModel, id=id)
    cart = CartItemModel(
        user=request.user,
        lunchbox=lunchbox,
        quantity=quantity,
    )
    cart.save()
    return redirect('hankki:lunchbox_list')



# ===========
#  Supplier
# ===========

@login_required
def supplier(request):
    if request.user.groups.filter(name="supplier").exists():
        return render(request, 'supplier.html')

    if request.method == 'POST':
        form = SupplierPermissionRequestForm(request.POST)
        if form.is_valid():
            request.user.groups.add(Group.objects.get(name="supplier"))
            return render(request, 'supplier.html')
    else:
        form = SupplierPermissionRequestForm()
    context = {'form': form}
    return render(request, 'request_permission.html', context)