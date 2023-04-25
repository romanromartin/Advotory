import random
from django.contrib.auth import authenticate, login, logout
import pyexcel_xlsx
import pyexcel_xls
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.core import serializers
from django.urls import reverse

from ArgoTrade.settings import CART_SESSION_ID
from django.contrib.auth.models import User

from argo.forms import *
from argo.models import *
import json

cat_all = Category.objects.all()
sub_all = Subcategory.objects.all()
var_all = Variation.objects.all()


def index(request):
    data = pyexcel_xls.get_data("static/input/st.xls")
    return render(request, 'index.html', context={'category': cat_all})


def category(request, id_category):
    cat_sel = Category.objects.get(id_category=id_category)
    sub_list = Subcategory.objects.filter(cat=cat_sel)
    prod_set = Product.objects.filter(cat=cat_sel)
    product_list = get_prod_list(prod_set)

    if request.method == 'POST':
        if request.POST.get("tocart"):
            add_to_cart(request)
    return render(request, 'category.html', context={'sub': sub_list, 'cat_sel': cat_sel,
                                                     'product_list': product_list})


def sub(request, id_category, id_sub):
    cat_sel = Category.objects.get(id_category=id_category)
    sub_sel = Subcategory.objects.get(id_sub=id_sub)
    prod_set = Product.objects.filter(sub_cat=Subcategory.objects.get(id_sub=id_sub))
    product_list = get_prod_list(prod_set)

    if request.method == 'POST':
        if request.POST.get("tocart"):
            add_to_cart(request)

    return render(request, 'sub.html', context={'all_var': var_all, 'product_list': product_list, 'sub_sel': sub_sel,
                                                'cat_sel': cat_sel})


def cart(request):
    # print(request.session.get(CART_SESSION_ID))
    item_list, total_price = make_product_list(request)
    if request.method == 'POST':
        if request.POST.get("order"):
            order = Order()
            order.article = make_random_artocle()
            if request.user.is_authenticated:
                order.user_order = request.user.username

            else:
                if request.POST.get("name"):
                    order.user_order = request.POST.get("name")
                order.phone = request.POST.get("phone")
            item_list = make_order_dict(request)
            order.order_json = json.dumps(item_list,  ensure_ascii=False )

            order.save()
            request.session[CART_SESSION_ID] = request.session.get(CART_SESSION_ID).clear()
            return redirect('index')

        if request.POST.get("delete"):
            if len(request.session.get(CART_SESSION_ID)) > 0:
                request.session.get(CART_SESSION_ID).pop(int(request.POST.get("delete")))
                request.session[CART_SESSION_ID] = request.session.get(CART_SESSION_ID)
    return render(request, 'cart.html', context={'item_list': item_list,
                                                 'total_price': total_price})


def managment(request):
    if request.method == 'POST':
        if request.POST.get("update"):
            Variation.objects.all().delete()
            Product.objects.all().delete()
            Subcategory.objects.all().delete()
            Category.objects.all().delete()
            Currancy.objects.all().delete()
            Producer.objects.all().delete()

            data = pyexcel_xls.get_data("static/input/st.xls")
            id_product_to_add = ''
            for cat in data['category']:
                Category(id_category=cat[0], category=cat[1], prw_category=cat[2]).save()
            for subc in data['subcategory']:
                Subcategory(id_sub=subc[0], sub=subc[1],
                            cat=Category.objects.get(id_category=subc[2]),
                            prw_sub=subc[3]).save()
            for prod in data['producer']:
                Producer(id_producer=prod[0], producer=prod[1]).save()
            for c in data['currancy']:
                Currancy(cur_name=c[0], cur_value=c[1]).save()

            prod_start = False
            ind = 1
            for pro in data['product']:

                # print(pro)
                if len(pro) > 0:
                    if pro[0] == 'id':
                        prod_start = True
                        continue
                    elif pro[0] == 'id':
                        continue
                    elif len(pro) < 5:
                        continue
                    elif pro[0] == 'variant':
                        default_now = False
                        if pro[10] != '' and pro[10] != ' ' and pro[10] != '-':
                            default_now = pro[10]
                        prod_cur = Product.objects.get(id_product=id_product_to_add).currancy.cur_value
                        Variation(prod=Product.objects.get(id_product=id_product_to_add),
                                  width=pro[7],
                                  sheet=pro[6],
                                  thicknes=pro[8],
                                  price=round(pro[9] * prod_cur),
                                  default=default_now,
                                  id=str(id_product_to_add) + '-' + str(ind),
                                  color=pro[15],
                                  power=pro[16]
                                  ).save()
                        ind += 1
                    elif pro[0] != '':
                        if prod_start:
                            id_product_to_add = pro[0]
                            if len(pro) < 6:
                                pro.append(True)
                            ind = 1

                            pr = Product(id_product=id_product_to_add,
                                         product=pro[1], prw_product=pro[2],
                                         producer=Producer.objects.get(id_producer=pro[4]),
                                         prod_float=pro[5],
                                         unit=pro[11],
                                         currancy=Currancy.objects.get(cur_name=pro[12]),
                                         matt=pro[14],

                                         )
                            if pro[3] != '-' and pro[3] != '' and pro != ' ':
                                pr.sub_cat = Subcategory.objects.get(id_sub=pro[3])
                            if pro[13] != '-' and pro[13] != '' and pro[13] != ' ':
                                pr.cat = Category.objects.get(id_category=pro[13])

                            pr.save()

    return render(request, 'managment.html')


def handler(request):

    if request.user.is_authenticated:
        all_orders = serializers.serialize('json', Order.objects.all())
        # all_orders = Order.objects.all()
        return render(request, 'handler.html', context={'all_orders': all_orders})
    else:
        next_url = 'handler'
        url = reverse('login')
        url_ = f'{url}?next={next_url}&'
        return redirect(url_)



def loginUser(request):
    if request.method == 'POST':
        form = LogInForm(data=request.POST)
        if request.method == 'POST':
            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get('username'),
                                    password=form.cleaned_data.get('password'))
                login(request, user)
                return redirect(request.GET['next'])
    else:
        form = LogInForm()
    return render(request, 'registration/login.html', {'form': form, })


def logoutUser(request):
    logout(request)
    return redirect(request.GET['next'])


def add_to_cart(request):
    foo = [[request.POST.get("option"), request.POST.get("quantity"), request.POST.get("matt_glossy")]]
    if request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] += foo
    else:
        request.session[CART_SESSION_ID] = foo


def get_prod_list(prod_set):
    product_list = []
    for pr in prod_set:
        to_add = [pr.id_product, pr.product, pr.prw_product.name, pr.unit, pr.prod_float, pr.producer.producer, pr.matt]
        to_add_var = []
        for var in Variation.objects.filter(prod=Product.objects.get(id_product=pr.id_product)):
            to_add_var.append(
                [var.id, var.width, var.sheet, var.thicknes, var.price, var.default, var.color, var.power])
        to_add.append(to_add_var)
        product_list.append(to_add)
    return product_list


def make_product_list(request):
    total_price = 0
    item_list = []
    list_index = 0
    if request.session.get(CART_SESSION_ID):
        for item in request.session.get(CART_SESSION_ID):
            var = Variation.objects.get(id=item[0])
            attr_text = ''
            if var.width != '-' and var.width != '':
                attr_text += 'Ширина ' + var.width
            if var.sheet != '-' and var.sheet != '':
                attr_text += 'Размер листа ' + var.sheet
            if var.thicknes != '-' and var.thicknes != '':
                attr_text += 'Толщина ' + var.thicknes
            matt = ''
            if item[2]:
                if item[2] == 'matt':
                    matt = 'Матовая'
                else:
                    matt = 'Глянцевая'
            parent = ''
            if var.prod.sub_cat:
                parent = var.prod.sub_cat.sub
            elif var.prod.cat:
                parent = var.prod.cat.category
            item_list.append([var.prod.product, var.prod.prw_product.name, parent,
                              'Цена ' + str(var.price) + ' за ' + var.prod.unit, matt,
                              '    Количество ' + item[1] + ' ' + var.prod.unit,
                              round(float(item[1]) * var.price), list_index,
                              attr_text, ])
            list_index += 1
            total_price += round(float(item[1]) * var.price)
    return item_list, total_price


def make_random_artocle():
    new_article = 0
    article_in_use_list = []
    for article_in_use in Order.objects.all():
        article_in_use_list.append(article_in_use.article)
    while new_article == 0:
        number = random.randrange(1000, 9999)
        if number not in article_in_use_list:
            new_article = number
    return new_article


def make_order_dict(request):
    item_list = []
    if request.session.get(CART_SESSION_ID):
        for item in request.session.get(CART_SESSION_ID):
            op = Variation.objects.get(id=item[0])
            if not op.prod.cat:
                parent = op.prod.sub_cat.sub
            else:
                parent = op.prod.cat.category
            item_dict = {'article': op.id,
                         'category': parent,
                         'name': op.prod.product,
                         'preview': op.prod.prw_product.name,
                         'price': op.price,
                         'width': op.width, 'thicknes': op.thicknes, 'sheet': op.sheet,
                         'color': op.color, 'power': op.power,
                         'quantity': item[1],
                         'matt': item[2],
                         'unit': op.prod.unit
                         }
            item_list.append(item_dict)
    return item_list
