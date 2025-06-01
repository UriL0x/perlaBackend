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
class DceascedView(viewsets.ModelViewSet):
    queryset = Dceasced.objects.all()
    serializer_class = DceascedSerializer    
    
    def list(self, request):
        dceasced = Dceasced.objects.all()
        dceasced = DceascedSerializer(dceasced, many=True).data
        docs = Document.objects.all()
        docs = DocumentSerializer(docs, many=True).data
        
        # Hacer que devuelva los muertos con sus documentos
        data = []
        for d in dceasced:
            docAsoc = []
            for doc in docs:
                if doc['dceased'] == d['id']:
                    docAsoc.append(doc)
            data.append({
                "dceasced": d, 
                "docs": docAsoc  
            })
        
        return Response({'dceasced': data}, status=status.HTTP_200_OK)
         
    def destroy(self, request, *args, **kwargs):
        # Obtener datos
        param = kwargs.get('pk')
        dceasced = Dceasced.objects.get(id=param)
        
         # Actualizar estado de la tumba
        if dceasced.grave:
            grave_id = dceasced.grave.id
            grave = Grave.objects.get(id=grave_id)
            grave.is_busy = False
            grave.save()
        
        dceasced.delete()
        return Response({'Difunto eliminado'}, status=status.HTTP_200_OK)
   
    def create(self, request):
        if len(request.data) == 0:
            return Response({"error": "Faltan campos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        name = request.data.get('name')
        second_name = request.data.get('second_name')
        date_of_death = request.data.get('date_of_death')
        files = request.FILES.getlist('documents')
        grave_num= int(request.data.get('grave'))
   
        # Validar tumba
        try:
            grave = Grave.objects.get(num=grave_num)
        except Grave.DoesNotExist:
            print("no existe")
            return Response({"error": "No existe una tumba con ese número"}, status=status.HTTP_400_BAD_REQUEST)
        if grave.is_busy:
            print("ta leno")
            return Response({"error": "Esta tumba ya esta ocupada"}, status=status.HTTP_400_BAD_REQUEST)
        grave.is_busy = True
        grave.save()
    
        # Save dceased in db
        dceasced = Dceasced()
        dceasced.name = name
        dceasced.second_name = second_name
        dceasced.date_of_death = date_of_death
        dceasced.grave = grave
        dceasced.save()
        
        # Save documents
        if files:
            for file in files:
                document = Document()
                document.route = file
                document.dceased = dceasced
                document.save()
                
        return Response({'Difuntos registrado'}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        print(request.data)
        param = kwargs.get('pk')
        try:
            dceasced = Dceasced.objects.get(id=param)
        except Dceasced.DoesNotExist:
            return Response({"error": "Difunto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar campos del difunto
        dceasced.name = request.data.get('name')
        dceasced.second_name = request.data.get('second_name')
        dceasced.date_of_death = request.data.get('date_of_death')

        # Obtener tumba actual y solicitada
        current_grave = dceasced.grave
        grave_num = request.data.get('grave')

        if str(grave_num) != str(current_grave.num):  # Si se intenta cambiar la tumba
            try:
                new_grave = Grave.objects.get(num=grave_num)
            except Grave.DoesNotExist:
                return Response({"error": "No existe una tumba con ese número"}, status=status.HTTP_400_BAD_REQUEST)

            if new_grave.is_busy:
                return Response({"error": "La tumba ya está ocupada"}, status=status.HTTP_400_BAD_REQUEST)

            # Liberar la tumba anterior
            current_grave.is_busy = False
            current_grave.save()

            # Ocupar la nueva tumba
            new_grave.is_busy = True
            new_grave.save()

            dceasced.grave = new_grave

        # Guardar el difunto
        dceasced.save()
        return Response({"mensaje": "Información actualizada"}, status=status.HTTP_200_OK)

class DocumentView(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    def create(self, request, *args, **kwargs):
        document = Document()
        dceasced = Dceasced.objects.get(id=request.data.get('dceasced'))
        document.dceased = dceasced
        document.route = request.FILES.get('route')
        document.save()
        serializer = DocumentSerializer(document)
        return Response({'doc': serializer.data}, status=status.HTTP_201_CREATED)
    
    @api_view(['GET'])
    def getDocsByDceasced(request):
        id_dceasced = request.data.get('dceasced')
        dceased = Dceasced.objects.get(id=id_dceasced)
        docs = Document.objects.filter(dceased=dceased)
        serializer = DocumentSerializer(docs, many=True)
        return Response({'documents': serializer.data}, status=status.HTTP_200_OK)