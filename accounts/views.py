from django.shortcuts import render
from rest_framework.views import APIView
from . serializers import RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework  import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.utils.encoding import force_str




 
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"user Registered Successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
       
 
 
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
       serializer  = LoginSerializer(data=request.data) 
       serializer.is_valid(raise_exception=True)
       
       user = serializer.validated_data['user']
       refresh =  RefreshToken.for_user(user)
       
       return Response({
           "message": "Login succesfull",
           "access":str(refresh.access_token),
           "refresh":str(refresh),
           "user": { "id": user.id,
                    "email": user.email,
                    "username": user.username, 
                    "role": user.role,
                    }
       },status=status.HTTP_200_OK)
       


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password:\n{reset_link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset link sent to your email"},
            status=status.HTTP_200_OK
        )



class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get("password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"message": "Invalid link"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"message": "Token expired or invalid"}, status=400)

        user.set_password(password)
        user.save()

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )
       
       

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Expect the refresh token in the request body
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                return Response(
                    {"detail": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ Adds the token to blacklist
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
       