
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from products.models import Product
from .permissions import IsAdmin
from orders.models import Order
from django.db.models import Count
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import AdminUserListSerializer, AdminUserDetailSerializer
from rest_framework import status
# Create your views here.

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        total_users = User.objects.count()
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        
        category_data =(Product.objects.values('category').annotate(count=Count('id'))) 
        
        user_orders = (User.objects.annotate(order_count = Count('orders')).values('username','order_count'))
        
        line_chart_data  = [
            {
                "name":user['username'],
                "orders":user['order_count']
            }
            for user in user_orders
        ]
        
        return Response({
            "counts":{
                "users":total_users,
                "products":total_products,
                "orders":total_orders
            },
            "categories":category_data,
            "user_orders":line_chart_data
        })
        
        
        



class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.filter(role="user").order_by("-date_joined")
        serializer = AdminUserListSerializer(users, many=True)
        return Response(serializer.data)
        
        
        
class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk, role="user")
        serializer = AdminUserDetailSerializer(user)
        return Response(serializer.data)
        
  
        
class AdminUserStatusToggleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        user = get_object_or_404(User, id=pk, role="user")

        user.status = "Inactive" if user.status == "Active" else "Active"
        user.save()

        return Response({
            "id": user.id,
            "status": user.status
        })
        
        


class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"detail": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Allowed transitions
        allowed_transitions = {
        "pending": ["paid", "cancelled", "delivered"],  # <-- allow direct deliver
        "paid": ["shipped"],
        "shipped": ["delivered"],
}


        # ❌ Final states   
        if order.status in ["delivered", "cancelled"]:
            return Response(
                {"detail": "Final order status cannot be changed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in allowed_transitions.get(order.status, []):
            return Response(
                {
                    "detail": f"Cannot change status from {order.status} to {new_status}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save(update_fields=["status"])

        return Response(
            {
                "id": order.id,
                "status": order.status,
                "message": "Order status updated successfully"
            },
            status=status.HTTP_200_OK
        )
       
    
       
class AdminOrderListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        orders = Order.objects.prefetch_related("items__product").all()

        data = []
        for order in orders:
            items_data = []
            for item in order.items.all():
                items_data.append({
                    "product_id": item.product.id,
                    "product_title": item.product.title,
                    "product_price": item.product.price,
                    "product_image": item.product.image,  # ✅ FIXED
                    "quantity": item.quantity,
                })

            data.append({
                "order_id": order.id,
                "user": order.user.email,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": order.created_at,
                "items": items_data,
            })

        return Response(data)

       