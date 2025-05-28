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
    location = serializers.SerializerMethodField()
    is_busy = serializers.BooleanField()
    row = RowSerializer(read_only=True)
    rows = RowSerializer(source='row_set', many=True, read_only=True)
    
    class Meta:
        model = Grave
        fields = '__all__' 
        
    def get_location(self, obj):
        return {
            'row':{obj.row.num}, 
            'section': {obj.row.section.num}, 
            'block': {obj.row.section.block.num}
            }       

class DceascedSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    grave = GraveSerializer()
    class Meta:
        model = Dceasced
        fields = '__all__'
        
    def get_location(self, obj):
        return {
            f'Tumba {obj.grave.num}, Fila {obj.grave.row.num}, Cuadro {obj.grave.row.section.num}, Manzana {obj.grave.row.section.block.num}'
            }
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    