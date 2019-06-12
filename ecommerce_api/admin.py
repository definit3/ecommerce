from django.contrib import admin
from .models import *

admin.site.register(Sellers)
admin.site.register(Items)
admin.site.register(SellersItems)
admin.site.register(Orders)
admin.site.register(Cart)

# Register your models here.
