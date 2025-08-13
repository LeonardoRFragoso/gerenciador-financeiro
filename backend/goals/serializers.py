from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """Serializer para metas"""
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    monthly_target = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'category', 'target_amount',
            'current_amount', 'target_date', 'status', 'priority',
            'is_public', 'auto_save', 'monthly_contribution',
            'progress_percentage', 'remaining_amount', 'is_completed',
            'days_remaining', 'monthly_target', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_monthly_target(self, obj):
        """Calcula o valor mensal necessário para atingir a meta"""
        return float(obj.get_monthly_target())
    
    def create(self, validated_data):
        # Associa automaticamente ao usuário logado
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GoalCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de metas"""
    
    class Meta:
        model = Goal
        fields = [
            'title', 'description', 'category', 'target_amount',
            'target_date', 'priority', 'is_public', 'auto_save',
            'monthly_contribution'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GoalContributionSerializer(serializers.Serializer):
    """Serializer para contribuições em metas"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    description = serializers.CharField(max_length=200, required=False)
    
    def validate_amount(self, value):
        """Valida se o valor da contribuição é válido"""
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value


class GoalSummarySerializer(serializers.Serializer):
    """Serializer para resumo de metas"""
    total_goals = serializers.IntegerField()
    active_goals = serializers.IntegerField()
    completed_goals = serializers.IntegerField()
    total_target_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_current_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_progress = serializers.FloatField()
    goals_by_priority = serializers.DictField()
    goals_by_category = serializers.DictField()
