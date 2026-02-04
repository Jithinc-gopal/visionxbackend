from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product,Category,Review
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,AllowAny, IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReviewSerializer
from orders.models import Order, OrderItem  
from django.shortcuts import get_object_or_404
 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
   
    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser] 
        
   


class ProductReviewView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        product = get_object_or_404(Product, id=product_id)
        
        order_items = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered' 
        )
        
        if not order_items.exists():
            return Response(
                {
                    "detail": "You must purchase and receive this product (status: delivered) before reviewing it.",
                    "has_purchased": False,
                    "is_delivered": False
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        for order_item in order_items:
            if hasattr(order_item, 'review'):
                return Response(
                    {
                        "detail": "You have already reviewed this product from your order.",
                        "order_id": order_item.order.id,
                        "has_reviewed": True
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Use the first delivered order item for review
        order_item = order_items.first()
        
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Create review with order_item reference
        review = Review.objects.create(
            product=product,
            user=request.user,
            order_item=order_item,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data["comment"]
        )
        
        return Response(
            ReviewSerializer(review, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )



class CanReviewProductView(APIView):
    """Check if user can review a specific product"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user has purchased and received the product
        purchased_items = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        )
        
        can_review = False
        order_item_id = None
        order_id = None
        
        if purchased_items.exists():
            # Check if any of the purchased items hasn't been reviewed yet
            for item in purchased_items:
                if not hasattr(item, 'review'):
                    can_review = True
                    order_item_id = item.id
                    order_id = item.order.id
                    break
        
        # Check if already reviewed
        has_reviewed = Review.objects.filter(
            user=request.user,
            product=product
        ).exists()
        
        return Response({
            'can_review': can_review and not has_reviewed,
            'has_purchased': purchased_items.exists(),
            'has_reviewed': has_reviewed,
            'order_item_id': order_item_id,
            'order_id': order_id,
            'product_id': product_id,
            'is_delivered': purchased_items.filter(order__status='delivered').exists()
        })


class UserReviewableView(APIView):
    """Get all products that user can review"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get all delivered order items for this user
        delivered_items = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered'
        ).select_related('product')
        
        reviewable_products = []
        
        for item in delivered_items:
            # Check if not already reviewed
            if not hasattr(item, 'review'):
                product_data = {
                    'product_id': item.product.id,
                    'product_title': item.product.title,
                    'product_image': item.product.image,
                    'order_id': item.order.id,
                    'order_item_id': item.id,
                    'purchased_date': item.order.created_at,
                    'purchased_quantity': item.quantity,
                    'purchased_price': float(item.price)
                }
                
                # Add absolute URL for image if needed
                request = self.request
                if request and hasattr(item.product.image, 'url'):
                    product_data['product_image_url'] = request.build_absolute_uri(item.product.image.url)
                
                reviewable_products.append(product_data)
        
        return Response({
            'count': len(reviewable_products),
            'products': reviewable_products
        })