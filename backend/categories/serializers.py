from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorias"""
    transaction_count = serializers.ReadOnlyField(source='get_transaction_count')
    total_amount = serializers.ReadOnlyField(source='get_total_amount')
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'type', 'color', 'icon',
            'is_active', 'transaction_count', 'total_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Associa automaticamente ao usuário logado
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de categorias"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'type', 'color', 'icon']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
