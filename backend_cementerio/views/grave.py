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
class GraveView(viewsets.ModelViewSet):
    queryset = Grave.objects.all()
    serializer_class = GraveSerializer
    
    def create(self, request):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        print(request.data)
        num_grave = request.data.get('num')
        num_row = request.data.get('row')
        
        # Validar tumba
        grave = Grave.objects.filter(num=num_grave)
        if grave:
            return Response({"error": "Ya existe una tumba con ese número"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar tumba
        row = Row.objects.get(num=num_row)
        grave = Grave()
        grave.num = num_grave
        grave.row = row
        grave.save()
       
        return Response({"Tumba registrada"}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        param = kwargs.get('pk')
        print(request.data)
        
        # Guadar numero y obteter tumba
        grave = Grave(id=param)
        grave.num = int(request.data.get('num'))
        
        # Revisar si hubo cambios en el estado
        is_busy = request.data.get('is_busy')
        if is_busy.lower() in 'true':
            grave.is_busy = True
            grave.save()
            
        # Actuaslizar ubicacion
        row = Row.objects.get(num=request.data.get('row'))
        grave.row = row        
        grave.save()

        return Response({"Tumba actualizada"}, status=status.HTTP_200_OK)