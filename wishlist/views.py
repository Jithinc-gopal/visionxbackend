from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from.models import WishlistItem
from .serializers import WishListItemSerializer
from rest_framework.response import Response
from products.models import Product
from rest_framework import status

# Create your views here.

    
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = WishlistItem.objects.filter(user=request.user)
        serializer = WishListItemSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        serializer = WishListItemSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get("product_id")

        try:
            item = WishlistItem.objects.get(
                user=request.user,
                product_id=product_id
            )
        except WishlistItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(
            {"message": "Item removed from wishlist"},
            status=status.HTTP_200_OK
        )
    
    
    
class WishlistCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = WishlistItem.objects.filter(user=request.user).count()
        return Response({"count": count})
