from rest_framework import serializers
from .models import Transaction
from categories.models import Category
from categories.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para transações"""
    category_details = CategorySerializer(source='category', read_only=True)
    formatted_amount = serializers.ReadOnlyField()
    tags_list = serializers.ReadOnlyField(source='get_tags_list')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'description', 'amount', 'formatted_amount', 'type',
            'payment_method', 'date', 'category', 'category_details',
            'notes', 'tags', 'tags_list', 'is_recurring', 'recurring_frequency',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Associa automaticamente ao usuário logado
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_category(self, value):
        """Valida se a categoria pertence ao usuário e é do tipo correto"""
        if value:
            user = self.context['request'].user
            if value.user != user:
                raise serializers.ValidationError("Categoria não encontrada.")
            
            # Valida tipo da categoria com tipo da transação
            transaction_type = self.initial_data.get('type')
            if transaction_type and value.type != transaction_type:
                raise serializers.ValidationError(
                    f"Categoria deve ser do tipo '{transaction_type}'"
                )
        return value


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de transações"""
    
    class Meta:
        model = Transaction
        fields = [
            'description', 'amount', 'type', 'payment_method', 'date',
            'category', 'notes', 'tags', 'is_recurring', 'recurring_frequency'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_category(self, value):
        if value:
            user = self.context['request'].user
            if value.user != user:
                raise serializers.ValidationError("Categoria não encontrada.")
        return value


class TransactionSummarySerializer(serializers.Serializer):
    """Serializer para resumo de transações"""
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_count = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()
