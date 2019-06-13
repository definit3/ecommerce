from django.urls import path, include
from ecommerce_api import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', views.SignupSubmit, name='signup'),
    path('', views.GetSellers, name='getSellers'),
    path('item',views.GetItems, name='getItems'),
    path('saveorders',views.SaveOrders, name='SaveOrders'),
    path('getorders',views.GetOrders, name='GetOrders'),
    path('getfullorders',views.GetFullOrders, name='GetFullOrders'),
    path('login',views.loginSubmit)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
