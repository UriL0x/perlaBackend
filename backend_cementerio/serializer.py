from rest_framework import serializers
from .models import CustomUser, Dceasced, Document, Grave, Section, Row, Block

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
class RowSerializer(serializers.ModelSerializer):    
    has_busy_grave = serializers.SerializerMethodField()

    class Meta:
        model = Row
        fields = ['id', 'num', 'has_busy_grave']

    def get_has_busy_grave(self, obj):
        return obj.grave_set.filter(is_busy=True).exists()

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
        grave = getattr(obj, 'grave', None)
        row = getattr(grave, 'row', None) if grave else None
        section = getattr(row, 'section', None) if row else None
        block = getattr(section, 'block', None) if section else None

        num = getattr(grave, 'num', '')
        row_num = getattr(row, 'num', '')
        section_num = getattr(section, 'num', '')
        block_num = getattr(block, 'num', '')

        return f'Tumba {num}, Fila {row_num}, Cuadro {section_num}, Manzana {block_num}'
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    