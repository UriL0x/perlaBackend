from rest_framework import serializers
from .models import Block, Section, Row, Grave, Dceasced

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'num']

class SectionSerializer(serializers.ModelSerializer):
    block_num = serializers.IntegerField(source='block.num', read_only=True)
    class Meta:
        model = Section
        fields = ['id', 'num', 'block_num']

class RowSerializer(serializers.ModelSerializer):
    section_num = serializers.IntegerField(source='section.num', read_only=True)
    block_num = serializers.IntegerField(source='section.block.num', read_only=True)
    class Meta:
        model = Row
        fields = ['id', 'num', 'section_num', 'block_num']

class GraveSerializer(serializers.ModelSerializer):
    row_num = serializers.IntegerField(source='row.num', read_only=True)
    section_num = serializers.IntegerField(source='row.section.num', read_only=True)
    block_num = serializers.IntegerField(source='row.section.block.num', read_only=True)
    class Meta:
        model = Grave
        fields = ['id', 'num', 'is_busy', 'row_num', 'section_num', 'block_num']

class DeceasedSerializer(serializers.ModelSerializer):
    grave_num = serializers.IntegerField(source='grave.num', read_only=True)
    block_num = serializers.IntegerField(source='grave.row.section.block.num', read_only=True)
    section_num = serializers.IntegerField(source='grave.row.section.num', read_only=True)
    row_num = serializers.IntegerField(source='grave.row.num', read_only=True)
    
    class Meta:
        model = Dceasced
        fields = ['id', 'name', 'second_name', 'date_of_death', 'grave_num', 'block_num', 'section_num', 'row_num']
