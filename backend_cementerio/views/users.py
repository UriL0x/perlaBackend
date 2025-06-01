from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..serializer import CustomUserSerializer, RowSerializer, SectionSerializer, BlockSerializer, DceascedSerializer, DocumentSerializer, GraveSerializer
from ..models import CustomUser, Dceasced, Document, Row, Grave, Block, Section
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    @api_view(['POST'])
    def ascend(request):
        # Obtener usuarios
        userToAscend = CustomUser.objects.get(id=request.data.get('id'))
        userAdmin = CustomUser.objects.get(is_admin=True)
        
        # Actulizar privilegios
        userAdmin.is_admin = False
        userAdmin.save()
        userToAscend.is_admin = True
        userToAscend.save()
        
        return Response({"Usuario ascendido"}, status=status.HTTP_200_OK)

    @api_view(['POST'])
    def register(request):
        username = request.data.get("username")
        password = request.data.get("password")
        is_admin = request.data.get("is_admin")
        
        if is_admin == 'admin':
            is_admin = True
        else:
            is_admin = False
      
        if not username or not password:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser(username=username, is_admin=is_admin)
        user.set_password(password)
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Usuario registrado correctamente",
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get("username")
        password = request.data.get("password")
        is_admin = request.data.get("is_admin")

        if username:
            user.username = username

        if password:
            user.set_password(password) 

        if is_admin is not None:
            user.is_admin = is_admin in [True, "true", "True", "1", 1]

        user.save()

        return Response({
            "message": "Usuario actualizado correctamente",
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }, status=status.HTTP_200_OK)
        
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Faltan credenciales"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        serializer = CustomUserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login exitoso",
            "token": token.key,
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

