from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from .models import HealthCategory, LunchboxModel
from .forms import HealthCategoryForm, LunchboxForm, SupplierPermissionRequestForm


def main(request):
    """메인 페이지"""
    lunchboxes = LunchboxModel.objects.all().order_by('-created')
    health_categories = HealthCategory.objects.all()
    context = {
        'lunchboxes': lunchboxes,
        'health_categories': health_categories,
    }
    return render(request, 'hankki/main.html', context)


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
            messages.success(request, '건강 카테고리가 저장되었습니다.')
            return redirect('hankki:main')
    else:
        form = HealthCategoryForm(instance=health_category)

    context = {'form': form}
    return render(request, 'hankki/health_category_form.html', context)


@login_required
@permission_required('hankki.lunchbox_supplier', login_url=reverse_lazy('hankki:supplier'))
def write_lunchbox(request, id=None):
    if id:
        lunchbox = get_object_or_404(LunchboxModel, id=id)
        if lunchbox.supplier != request.user:
            messages.error(request, '본인의 상품만 수정할 수 있습니다.')
            return redirect('hankki:main')
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
            messages.success(request, '도시락 상품이 저장되었습니다.')
            return redirect('hankki:main')
    else:
        form = LunchboxForm(instance=lunchbox)

    context = {'form': form, 'is_edit': id is not None}
    return render(request, 'hankki/lunchbox_form.html', context)


@login_required
def supplier(request):
    """판매자 권한 요청 및 판매자 페이지"""
    # 이미 판매자 그룹에 속해있으면 판매자 페이지 표시
    if request.user.groups.filter(name="supplier").exists():
        user_lunchboxes = LunchboxModel.objects.filter(supplier=request.user).order_by('-created')
        context = {'lunchboxes': user_lunchboxes}
        return render(request, 'hankki/supplier.html', context)

    if request.method == 'POST':
        form = SupplierPermissionRequestForm(request.POST)
        if form.is_valid():
            # 그룹이 없으면 생성, 있으면 가져오기
            group, created = Group.objects.get_or_create(name="supplier")
            request.user.groups.add(group)

            # 판매자 권한도 부여
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType
            content_type = ContentType.objects.get_for_model(LunchboxModel)
            permission, _ = Permission.objects.get_or_create(
                codename='lunchbox_supplier',
                name='도시락 판매자',
                content_type=content_type,
            )
            request.user.user_permissions.add(permission)

            messages.success(request, '판매자 권한이 부여되었습니다.')
            return redirect('hankki:supplier')
    else:
        form = SupplierPermissionRequestForm()

    context = {'form': form}
    return render(request, 'hankki/request_permission.html', context)