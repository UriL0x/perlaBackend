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
class BlockView(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    
    def create(self, request):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        num = request.data.get('num')
        
        # Ver si ya existe una secion con ese numero
        if Block.objects.filter(num=num).first():
           return Response({"error": "Ya existe una manzana con ese numero"}, status=status.HTTP_400_BAD_REQUEST)       
        
        # Guardar Bloque
        block = Block.objects.create(
            num = num
        )       

        return Response({
            "section": {
                "id": block.id,
                "num": block.num,
            }
        }, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class SectionView(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    
    def create(self, request):
        print(request.data)
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        num = request.data.get('num')
        block_id = request.data.get('block')
        
        # Ver si ya existe una secion con ese numero
        block = Block.objects.get(id=block_id)
        sections = block.section_set.all()
        for section in sections:
            if section.num == int(num):
                return Response({"error": "Ese cuadro ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar seccion
        section = Section.objects.create(
            num = num,
            block = block
        )       

        return Response({
            "section": {
                "id": section.id,
                "num": section.num,
                "block": section.block.id,
            }
        }, status=status.HTTP_201_CREATED)

        
    def update(self, request, *args, **kwargs):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        param = kwargs.get('pk')
        row = Row.objects.get(id=param)
        if not row:
            return Response({"error": "No existe esta seccion"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ver si ya existe una seccion con ese numero
        num = request.data.get('num')
        block_id = request.data.get('block')
        block = Block.objects.get(id=block_id)
        sections = block.section_set.all()
        for section in sections:
            if section.num == int(num):
                return Response({"error": "La seccion ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        section.num = num
        section.save()

        return Response({"SEccion actualizada"}, 
                        status=status.HTTP_201_CREATED)
 
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])   
class RowView(viewsets.ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializer
    
    def create(self, request):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        num = request.data.get('num')
        section_id = request.data.get('section')
        
        # Ver si ya existe una fila con ese numero
        section = Section.objects.get(id=section_id)
        rows = section.row_set.all()
        for row in rows:
            if row.num == int(num):
                return Response({"error": "La fila ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar fila
        row = Row.objects.create(
            num = num,
            section = section
        )       

        serializer = RowSerializer(row)
        return Response({"row": serializer.data}, 
                        status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        param = kwargs.get('pk')
        row = Row.objects.get(id=param)
        if not row:
            return Response({"error": "No existe esta fila"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ver si ya existe una fila con ese numero
        num = request.data.get('num')
        section_id = request.data.get('section')
        section = Section.objects.get(id=section_id)
        rows = section.row_set.all()
        for row in rows:
            if row.num == int(num):
                return Response({"error": "La fila ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        row.num = num
        row.save()

        return Response({"Fila actualizada"}, 
                        status=status.HTTP_201_CREATED)
    
