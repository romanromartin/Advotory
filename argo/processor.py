from .models import *


def all_categorys(request):
    return {'category': Category.objects.all()}

def all_sub(request):
    return {'subcategory': Subcategory.objects.all()}

