from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    full_name = serializers.ReadOnlyField()
    total_balance = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'birth_date', 'monthly_income', 'currency',
            'email_notifications', 'push_notifications', 'total_balance',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_total_balance(self, obj):
        """Calcula o saldo total do usuário"""
        return float(obj.get_total_balance())


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de novos usuários"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'birth_date'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil do usuário (mais detalhado)"""
    full_name = serializers.ReadOnlyField()
    total_balance = serializers.SerializerMethodField()
    transaction_count = serializers.SerializerMethodField()
    goals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'birth_date', 'monthly_income', 'currency',
            'email_notifications', 'push_notifications', 'total_balance',
            'transaction_count', 'goals_count', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login']
    
    def get_total_balance(self, obj):
        return float(obj.get_total_balance())
    
    def get_transaction_count(self, obj):
        return obj.transactions.count()
    
    def get_goals_count(self, obj):
        return obj.goals.count()
