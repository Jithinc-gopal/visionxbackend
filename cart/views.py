from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework import status


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).order_by("id")
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

   
    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"},status=status.HTTP_204_NO_CONTENT)




class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # UPDATE QUANTITY
    def put(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")

        if quantity < 1:
            cart_item.delete()
            return Response({"message": "Item removed"})

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    # REMOVE ITEM
    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Item removed"})




class CartCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = CartItem.objects.filter(user=request.user).count()
        return Response({"count": count})
    
    
 
class sampleView(APIView):
    def get(self,request):
        return Response({"message":"ci/cd implimentation"})    