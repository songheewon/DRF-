from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from product.models import Product
from DRF.permissions import IsAdminOrIsAuthenticatedReadOnly
from product.serializers import ProductSerializer
from django.utils import timezone
from django.db.models import Q


# Create your views here.
class ProductView(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            products = Product.objects.filter(
                Q(exposure_end__gte=timezone.now(),
                  is_active=True) | Q(seller=user)
            )
            product_serializer = ProductSerializer(products, many=True).data
        else:
            products = Product.objects.filter(
                Q(exposure_end__gte=timezone.now(),
                  is_active=True)
            )
            product_serializer = ProductSerializer(products, many=True).data

        return Response(product_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data
        data['seller'] = user.id
        product_serializer = ProductSerializer(data=data, context={"request": request})

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        data = request.data
        product = Product.objects.get(id=obj_id)
        product_serializer = ProductSerializer(product, data=data, partial=True, context={"request": request})
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)