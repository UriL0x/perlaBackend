from rest_framework import serializers
from .models import CustomUser, Dceasced, Document, Grave, Section, Row, Block

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
class RowSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Row
        fields = ['id', 'num']

class SectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(source='row_set', many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'num', 'rows']

class BlockSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(source='section_set', many=True, read_only=True)

    class Meta:
        model = Block
        fields = ['id', 'num', 'sections']

class GraveSerializer(serializers.ModelSerializer):
    is_busy = serializers.BooleanField()
    row = RowSerializer(read_only=True)
    rows = RowSerializer(source='row_set', many=True, read_only=True)
    
    class Meta:
        model = Grave
        fields = '__all__'        

class DceascedSerializer(serializers.ModelSerializer):
    grave = GraveSerializer()
    class Meta:
        model = Dceasced
        fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    