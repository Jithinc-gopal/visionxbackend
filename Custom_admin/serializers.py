from rest_framework import serializers
from accounts.models import User
from orders.serializers import OrderSerializer

class AdminUserListSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(source='orders.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'status',
            'role',
            'orders_count'
        ]


class AdminUserDetailSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'status',
            'role',
            'date_joined',
            'orders'
        ]
