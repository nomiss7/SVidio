from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.catalog.models import Product
from apps.order.forms import AddToCartForm, CreateOrderForm
from apps.order.models import Cart, OrderProduct
from config.settings import PAGE_NAMES


def get_cart_data(user):
    cart = Cart.objects.filter(user=user)
    total = 0
    for row in cart:
        total += row.product.price * row.quantity
    return {'cart': cart, 'total': total}


def check_quantity(quantity, product):
    if quantity > product.quantity:
        return product.quantity
    return quantity


@login_required()
def add_to_cart(request):
    breadcrumbs = {'current': PAGE_NAMES['cart']}
    data = request.GET.copy()
    data.update(user=request.user)
    request.GET = data
    form = AddToCartForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        csrf = request.session.get('cart_token')
        if not csrf or csrf != data.get('csrfmiddlewaretoken'):
            row = Cart.objects.filter(product=cd['product'], user=cd['user']).first()
            if row:
                quantity = row.quantity + cd['quantity']
                Cart.objects.filter(id=row.id).update(quantity=check_quantity(quantity, cd['product']))
            else:
                form.quantity = check_quantity(cd['quantity'], cd['product'])
                form.save()
            request.session['cart_token'] = data.get('csrfmiddlewaretoken')
        return render(request, 'order/added.html', {'cart': get_cart_data(request.user), 'product': cd['product'],
                                                    'breadcrumbs': breadcrumbs})


@login_required
def cart_list(request):
    breadcrumbs = {'current': PAGE_NAMES['cart']}
    return render(request, 'order/cart_list.html', {'cart': get_cart_data(request.user),
                                                    'breadcrumbs': breadcrumbs})


@login_required()
def delete_from_cart(request, row_id):
    Cart.objects.filter(id=row_id).delete()
    breadcrumbs = {'current': PAGE_NAMES['cart']}
    return render(request, 'order/cart_list.html', {'cart': get_cart_data(request.user),
                                                    'breadcrumbs': breadcrumbs})


@login_required
def create_order(request):
    error = None
    user = request.user
    cart = get_cart_data(user)

    if not cart['cart']:
        return redirect('home')

    if request.method == 'POST':
        data = request.POST.copy()
        data.update(user=user, total=cart['total'])
        request.POST = data
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save()
                for row in cart['cart']:
                    OrderProduct.objects.create(
                        order=order,
                        product=row.product,
                        quantity=check_quantity(row.quantity, row.product),
                        price=row.product.price
                    )
                    Product.objects.filter(id=row.product.id)\
                        .update(quantity=row.product.quantity - check_quantity(row.quantity, row.product))
                Cart.objects.filter(user=user).delete()
            breadcrumbs = {'current': PAGE_NAMES['created_order']}
            return render(request, 'order/created.html', {'breadcrumbs': breadcrumbs})
        error = form.errors
    else:
        form = CreateOrderForm(data={
            'first_name': user.first_name if user.first_name else '',
            'last_name': user.last_name if user.last_name else '',
            'email': user.email if user.email else '',
            'phone': user.phone if user.phone else '',
        })
    breadcrumbs = {reverse('cart_list'): PAGE_NAMES['cart']}
    breadcrumbs.update({'current': PAGE_NAMES['order']})
    return render(request, 'order/create.html', {'cart': cart, 'form': form, 'error': error,
                                                 'breadcrumbs': breadcrumbs})
