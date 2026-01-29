from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk, user=request.user)
            serializer = OrderSerializer(order, context={"request": request})
            return Response(serializer.data)

        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)


    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Calculate total_price using ORM
        total_price = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0

        discount = 200 if total_price > 2000 else 0
        final_amount = total_price - discount

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            discount=discount,
            final_amount=final_amount,
            **serializer.validated_data
        )

        # Bulk create OrderItems
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in cart_items.select_related('product')
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear cart
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def patch(self, request, pk): 
        order = get_object_or_404(Order, pk=pk, user=request.user)

        if order.status != "pending":
            return Response({"detail": "Order cannot be cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "cancelled"
        order.save()
        return Response({"detail": "Order cancelled successfully"}, status=status.HTTP_200_OK)
