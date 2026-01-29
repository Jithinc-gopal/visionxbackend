from rest_framework import serializers
from .models import Order, OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="product.title", read_only=True
    )
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_title",
            "product_image",
            "quantity",
            "price",
        ]
        
    def get_product_image(self, obj):
        request = self.context.get("request")
        image = obj.product.image

        if not image:
            return None

        # ✅ If image is ImageFieldFile
        if hasattr(image, "url"):
            url = image.url
        else:
            # ✅ If image is already a string
            url = image

        if request:
            return request.build_absolute_uri(url)

        return url



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "full_name",
            "phone_number",
            "street_address",
            "city",
            "state",
            "pincode",
            "payment_method",
            "total_price",
            "discount",
            "final_amount",
            "status",
            "created_at",
            "items",
        ]
        read_only_fields = [
            "total_price",
            "discount",
            "final_amount",
            "status",
            "created_at",
        ]


