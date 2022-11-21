import json

from django.views.generic import DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Value, Sum

import stripe

from .models import Item, CurrencyUSDRate
from project.settings import STRIPE_SK, STRIPE_PK
from project.settings import STRIPE_SUCCESS_URL, STRIPE_CANCEL_URL


def get_products_queryset(pk_list, **kwargs):
    """Создаю queryset с необходимыми полями."""
    # если pk_list пустой, то возвращаем все товары
    pk_filter = ({'pk__in': pk_list} if pk_list else {'pk__gte': '0'})
    if kwargs.get('currency'):
        # если задана валюта, то добавляем поле валюта и цена в этой валюте
        current_currency_rate = CurrencyUSDRate.objects.\
            filter(name=kwargs.get('currency')).first().rate
        return Item.objects.all().filter(**pk_filter).\
            annotate(current_currency=Value(kwargs.get('currency'))).\
            annotate(currency_price=current_currency_rate*F('price')/F('currency__rate'))
    # если не задана валюта, то добавляем поле валюта и цена в валюте товара
    return Item.objects.all().filter(**pk_filter).\
        annotate(current_currency=F('currency__name')).\
        annotate(currency_price=F('price'))


def create_stripe_session(pk_list, **kwargs):
    """Создает и возвращает stripe сессию для товаров из списка."""
    li = []
    products = get_products_queryset(
        pk_list, currency=kwargs.get('currency', None))
    for prod in products:
        li.append({
            'price_data': {
                'currency': prod.current_currency,
                'product_data': {
                    'name': prod.title,
                    'description': prod.description,
                },
                "tax_behavior": "exclusive",
                'unit_amount': int(prod.currency_price*100),
            },
            'quantity': 1,
            'tax_rates': [
                "txr_1M5ux9KJ0E7HxxZYlK0jrswZ",
            ],
        })
    di = []
    if kwargs.get('coupon'):
        di.append({'coupon': kwargs.get('coupon')},)
    sp = dict(
        line_items=li,
        mode='payment',
        locale='ru',
        discounts=di,
        success_url=STRIPE_SUCCESS_URL,
        cancel_url=STRIPE_CANCEL_URL,
        tax_id_collection={'enabled': True},
    )
    stripe.api_key = STRIPE_SK
    return stripe.checkout.Session.create(**sp)


def session_to_json(request, pk):
    """Упаковываем и отдаем сессию в json формате."""
    session = create_stripe_session([pk])
    return HttpResponse(json.dumps(session))


class IndexListView(ListView):
    """Главная страница - список всех товаров."""

    model = Item
    current_currency = 'rub'

    def post(self, request, *args, **kwargs):
        self.current_currency = request.POST.get('currency', 'rub')
        if request.POST.get('buy_ident') or request.POST.get('buy_session'):
            pk_list = [k[3:] for k in request.POST.keys() if 'cb-' in k]

            if len(pk_list) > 0:
                # выбрано >1 товара
                if request.POST.get('buy_ident'):
                    # платеж методом PaymentIntent
                    # получаем покупателя
                    email = request.POST.get('email')
                    stripe.api_key = STRIPE_SK
                    customer_data = stripe.Customer.list(email=email).data

                    if len(customer_data) > 0:
                        # рассчитываем сумму платежа
                        products = get_products_queryset(
                            pk_list, currency=self.current_currency)
                        order_amount = int(products.aggregate(
                            Sum('currency_price'))['currency_price__sum'])*100

                        # производим оплату
                        res = stripe.PaymentIntent.create(
                            customer=customer_data[0], amount=order_amount,
                            currency=self.current_currency, confirm=True,)
                        res = json.loads(str(res))
                        if res['status'] == 'succeeded':
                            return HttpResponseRedirect(reverse('items:success'))
                else:
                    # платеж методом Session
                    session = create_stripe_session(
                        pk_list=pk_list,
                        currency=self.current_currency,
                        coupon=request.POST.get('coupon')
                    )
                    return HttpResponseRedirect(session.url)
            # не удается выполнить платеж
            return HttpResponseRedirect(reverse('items:cancel'))
        # нет платежей. просто пересчитали под другую валюту
        return self.get(request)

    def get_queryset(self):
        return get_products_queryset([], currency=self.current_currency)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_currency'] = self.current_currency
        context['currency'] = CurrencyUSDRate.objects.all().order_by('name')
        return context


class ProdDetailView(DetailView):
    """Страница покупки одного товара."""

    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STRIPE_PK'] = STRIPE_PK
        return context
