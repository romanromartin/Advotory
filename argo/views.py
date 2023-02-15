import pyexcel_xlsx
import pyexcel_xls
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.core import serializers
from ArgoTrade.settings import CART_SESSION_ID

from argo.models import *
import json

cat_all = Category.objects.all()
sub_all = Subcategory.objects.all()
var_all = Variation.objects.all()


def index(request):
    data = pyexcel_xls.get_data("static/input/st.xls")
    return render(request, 'index.html', context={})


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
    sub_sel = Subcategory.objects.get(id_sub=id_sub)
    prod_set = Product.objects.filter(sub_cat=Subcategory.objects.get(id_sub=id_sub))
    product_list = get_prod_list(prod_set)

    if request.method == 'POST':
        if request.POST.get("tocart"):
            add_to_cart(request)

    return render(request, 'sub.html', context={'all_var': var_all, 'product_list': product_list, 'sub_sel': sub_sel})


def cart(request):
    # print(request.session.get(CART_SESSION_ID))
    total_price = 0

    if request.method == 'POST':
        if request.POST.get("delete"):
            request.session.get(CART_SESSION_ID).pop(int(request.POST.get("delete")))
            request.session[CART_SESSION_ID] = request.session.get(CART_SESSION_ID)


    item_list = []
    list_index = 0
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
    # print(item_list)
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
                                  id=str(id_product_to_add) + '-' + str(ind)
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
                                         matt=pro[14]
                                         )
                            if pro[3] != '-' and pro[3] != '' and pro != ' ':
                                pr.sub_cat = Subcategory.objects.get(id_sub=pro[3])
                            if pro[13] != '-' and pro[13] != '' and pro[13] != ' ':
                                pr.cat = Category.objects.get(id_category=pro[13])

                            pr.save()

    return render(request, 'managment.html')


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
            to_add_var.append([var.id, var.width, var.sheet, var.thicknes, var.price, var.default, var.color])
        to_add.append(to_add_var)
        product_list.append(to_add)
    return product_list
