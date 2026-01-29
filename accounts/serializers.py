from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True,min_length = 5)
    class Meta:
        model = User
        fields = ['username','email','password']
        
    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    
    def validate(self,data):
        user = authenticate(
            email = data['email'],
            password= data['password']
        )
        
        if not user:
            raise serializers.ValidationError("Invalied email or password")
        if user.status != "Active":
            raise serializers.ValidationError("User account is Inactive")
        
        data['user']= user
        return data
            


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "image",
            "date_joined",
        ]
        read_only_fields = ["email"]
 

 