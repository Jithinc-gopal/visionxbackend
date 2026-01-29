from rest_framework import serializers
from .models import Category,Product,Review
from orders.serializers import OrderItemSerializer  # Import if needed


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source= "category.name",read_only= True)
    
    class Meta:
        model = Product
        fields = [
             "id",
            "title",
            "description",
            "price",
            "image",
            "category",
            "category_name",
        ]        

# products/serializers.py

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.username", read_only=True
    )
    can_edit = serializers.SerializerMethodField()
    order_info = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user_name",
            "rating",
            "comment",
            "created_at",
            "can_edit",
            "order_info",
            "order_item",  # Keep for admin purposes
        ]
        read_only_fields = ["user_name", "created_at", "can_edit", "order_info"]

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.user == request.user
        return False

    def get_order_info(self, obj):
        if obj.order_item:
            return {
                "order_id": obj.order_item.order.id,
                "purchased_date": obj.order_item.order.created_at
            }
        return None