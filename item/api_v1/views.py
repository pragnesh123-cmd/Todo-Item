from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from item.models import Item
from item.api_v1.serializers import ItemSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters


# Create your views here.
class ItemViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "name"
    ]

    def get_queryset(self):
        queryset = super(ItemViewSet, self).get_queryset()
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            ItemSerializer(instance).data, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(
            data=ItemSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
