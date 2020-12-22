from django.shortcuts import render

from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework import filters

from .models import Product, Stock
from .serializer import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class ProductView2(APIView):
    @staticmethod
    def get(request):
        result = Product.objects.all()
        serializer = ProductSerializer(instance=result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        get_phone_number = request.data.get('phone_number')
        get_name = request.data.get('name')
        get_total_bonus = request.data.get('total_bonus')
        get_card_number = request.data.get('card_number')
        if not isinstance(get_card_number, str) or len(get_card_number) > 16:
            return Response('card number must be a string. max length 16', status=status.HTTP_400_BAD_REQUEST)
        get_count = request.data.get('count')
        if  not isinstance(get_count, int) or get_count < 0 or get_count > 32767:
            return Response('count must be integer in range(0, 32767)', status=status.HTTP_400_BAD_REQUEST
        if not isinstance(get_total_bonus, int):
            return Response('total bonus must be integer', status=status.HTTP_400_BAD_REQUEST)
        instance = Product.objects.create(phone_number=get_phone_number, name=get_name, total_bonus=get_total_bonus, card_number=get_card_number, count=get_count)
        return Response('created', status=status.HTTP_201_CREATED)

class ProductViewDetail2(APIView):
    def get(self, request, pk):
        result = Product.objects.get(pk=pk)
        return Response({"phone_number": result.phone_number, "name": result.name, "total_bonus": result.total_bonus, 
                        "card_number": result.card_number, "id": result.id, "count": result.count,
                        "date": result.date.strftime('%d.%m.%Y %H:%M')}, status=status.HTTP_200_OK)

class delete(self, request, pk):
    Product.objects.get(pk=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
                get_phone_number = request.data.get('phone_number')
        get_name = request.data.get('name')
        get_total_bonus = request.data.get('total_bonus')
        get_card_number = request.data.get('card_number')
        if not isinstance(get_card_number, str) or len(get_card_number) > 16:
            return Response('card number must be a string. max length 16', status=status.HTTP_400_BAD_REQUEST)
        get_count = request.data.get('count')
        if  not isinstance(get_count, int) or get_count < 0 or get_count > 32767:
            return Response('count must be integer in range(0, 32767)', status=status.HTTP_400_BAD_REQUEST
        if not isinstance(get_total_bonus, int):
            return Response('total bonus must be integer', status=status.HTTP_400_BAD_REQUEST)
        result.phone_number = get_phone_number
        result.name = get_name
        result.total_bonus = get_total_bonus
        result.card_number = get_card_number
        result.count = get_count
        result.save()
        return Response({"phone_number": result.phone_number, "name": result.name, "total_bonus": result.total_bonus, 
                        "card_number": result.card_number, "id": result.id, "count": result.count,
                        "date": result.date.strftime('%d.%m.%Y %H:%M')}, status=status.HTTP_200_OK)



class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('result', data),
        ]))


class ProductView(ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number', 'name', 'total_bonus', 'card_number', 'count']

    def get_queryset(self):
        queryset = Product.objects.all()
        order_field = self.request.GET.get('order')
        filter_fields = {}
       
        if self.request.GET.get('total_bonus'):
            filter_fields['total_bonus'] = self.request.GET.get('total_bonus')

        if self.request.GET.get('name'):
            filter_fields['name'] = self.request.GET.get('name')

        if self.request.GET.get('count'):
            filter_fields['count'] = self.request.GET.get('count')

        if order_field:
            queryset = queryset.order_by(order_field)

        if filter_fields:
            queryset = queryset.filter(**filter_fields)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            queryset = queryset.filter(date__date__gte=start_date, date__date__lte=end_date)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        stock = Stock.objects.first()
        stock.product_count += int(request.data['count'])
        stock.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        stock = Stock.objects.first()
        stock.product_count -= instance.count
        stock.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        stock = Stock.objects.first()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        stock.product_count -= instance.count
        stock.product_count += int(request.data['count'])
        stock.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
