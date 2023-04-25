from .models import *
from django.core import serializers


def all_categorys(request):
    data = serializers.serialize("json", Category.objects.all())
    return {'catjson': data}



def all_sub(request):
    data = serializers.serialize("json", Subcategory.objects.all())
    return {'subjson': data}



