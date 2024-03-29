from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ecommerce_api.models import *
import json
from django.contrib.auth import authenticate, login, logout
import logging
import sys
import uuid
import smtplib
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

class GetSellersAPI(APIView):

    def get(self, request, *args, **kwargs):
        response = {}
        response['status'] = 500
        try:
            sellers = Sellers.objects.all()
            seller_list = []
            for seller in sellers:
                temp = {}
                temp['id']=seller.seller_id
                temp['title']=seller.seller_name
                temp['tagline']=seller.seller_tagline
                temp['address']=seller.seller_address
                temp['image']=seller.seller_image.url
                seller_list.append(temp)
                print (temp)
            response['status'] = 200
            response['sellers'] = seller_list
        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in GetSellersAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)


class GetItemsAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            data = request.data
            id = data['id']
            seller_obj = Sellers.objects.get(seller_id=id)
            items_get = SellersItems.objects.filter(seller=seller_obj)
            seller_item_list = []
            for item_get in items_get:
                temp = {}
                temp['seller_name']=item_get.seller.seller_name
                temp['seller_id']=item_get.seller.seller_id
                temp['item_id']=item_get.item.item_id
                temp['item_name']=item_get.item.name
                temp['count']=item_get.count
                temp['image']=item_get.item.item_image.url
                temp['Price'] = item_get.item.item_price
                temp['Previous_Price'] = item_get.item.item_previous_price
                print (temp)
                seller_item_list.append(temp)
            response['status'] = 200
            response['items'] = seller_item_list
        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in GetItemsAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)


class SaveOrdersAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            data = request.data
            cart_items = data['cart_items']
            user_id = data['user_id']
            price = data['totalammount']
            buyer_obj = Sellers.objects.get(seller_id=user_id)

            new_order_id = uuid.uuid1()
            logger.info(cart_items)
            for item in cart_items:
                seller_id = item['seller_id']
                logger.info(seller_id)
                item_id = item['item_id']
                quantity = item['qty']
                logger.info("user_id: %s", user_id)
                logger.info("item_id: %s", item_id)
                logger.info("quantity: %s", quantity)
                logger.info("price: %s", price)
                item_obj = Items.objects.get(item_id=item_id)
                cart_obj = Cart(item=item_obj,count=quantity)
                cart_obj.save()
                new_order_obj = Orders(buyer = buyer_obj, order_id = new_order_id , cart=cart_obj, price=price)
                new_order_obj.save()

            response['order_id']=new_order_id
            response['status'] = 200

            seller_obj = Sellers.objects.get(seller_id=seller_id)
            seller_email = seller_obj.seller_email
            s = smtplib.SMTP('smtp.gmail.com',587)  #enter mail server host and port number
            s.starttls()
            s.login("roguedoppelganger@gmail.com", "02htcdesireC") #enter your email id and password.
            message = "Your have received a new order. Please approve or decline it! "
            s.sendmail("roguedoppelganger@gmail.com",seller_email, message)
            s.quit()

        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in SaveOrdersAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)



class GetOrdersAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            data = request.data
            user_id = data['user_id']
            buyer_obj = Sellers.objects.get(seller_id=user_id)
            orders = Orders.objects.values('order_id', 'price', 'date').distinct()
            logger.info(orders)
            order_list = []
            for order in orders:
                temp = {}
                temp['order_id']=order["order_id"]
                temp['price']=order["price"]
                temp['date']=order["date"]
                order_list.append(temp)
            response['status'] = 200
            response['orders'] = order_list

        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in GetOrdersAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)


class GetFullOrdersAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            data = request.data
            order_id = data['order_id']
            orders = Orders.objects.filter(order_id=order_id)
            logger.info(orders)
            order_list = []
            for order in orders:
                temp = {}
                temp['item_id']=order.cart.item.item_id
                temp['item_name']=order.cart.item.name
                temp['item_price']=order.cart.item.item_price
                temp['item_image'] = order.cart.item.item_image.url
                temp['count']=order.cart.count
                logger.info(temp)
                order_list.append(temp)
            response['status'] = 200
            response['orders'] = order_list
            logger.info(response)

        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in GetFullOrders: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)



class LoginSubmitAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            data = request.data
            username = data['username']
            password = data['password']
            print (username)
            print (password)
            user = authenticate(username=username, password=password)
            print (username)
            print (password)
            login(request, user)
            response['status'] = 200
        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in LoginSubmitAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))
        return Response(data=response)

class SignupSubmitAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response['status'] = 500
        try:
            data = request.data
            email = data['email']
            password = data['password']
            name = data['name']
            Temp = User.objects.filter(username =email)
            print(Temp)
            if len(Temp) == 0:
                user_obj = User.objects.create_user(username=email, password=password)
                seller_id = uuid.uuid1()
                seller_obj = Sellers.objects.create(seller_email=email, seller_id = seller_id, user=user_obj, seller_name=name)
                seller_obj.save()
                response['status'] = 200
                response['message'] = "ID created successfully"
            else :
                response['message'] = "email-id already exists"

        except Exception as e:
            e_type, e_object, e_tb = sys.exc_info()
            logger.error("Error in SignupSubmitAPI: %s at line no: %s", str(e), str(e_tb.tb_lineno))

        return Response(data=response)

SignupSubmit=SignupSubmitAPI.as_view()
loginSubmit=LoginSubmitAPI.as_view()
GetSellers=GetSellersAPI.as_view()
GetItems=GetItemsAPI.as_view()
SaveOrders = SaveOrdersAPI.as_view()
GetOrders = GetOrdersAPI.as_view()
GetFullOrders = GetFullOrdersAPI.as_view()
