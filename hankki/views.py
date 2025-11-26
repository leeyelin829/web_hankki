from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from .models import HealthCategory, LunchboxModel
from .forms import HealthCategoryForm, LunchboxForm, SupplierPermissionRequestForm


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



@login_required
@permission_required('lunchbox_supplier', login_url=reverse_lazy('hankki:supplier'))
def write_lunchbox(request, id=None):
    if id:
        lunchbox = get_object_or_404(LunchboxModel, id=id)
        if lunchbox.supplier != request.user:
            return redirect('/')
    else:
        lunchbox = None

    if request.method == 'POST':
        form = LunchboxForm(request.POST, instance=lunchbox)

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