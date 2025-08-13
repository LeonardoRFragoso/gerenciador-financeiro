from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de categorias"""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Usuários só veem suas próprias categorias
        return Category.objects.filter(user=self.request.user, is_active=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        return CategorySerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Retorna categorias agrupadas por tipo"""
        income_categories = self.get_queryset().filter(type='income')
        expense_categories = self.get_queryset().filter(type='expense')
        
        return Response({
            'income': CategorySerializer(income_categories, many=True).data,
            'expense': CategorySerializer(expense_categories, many=True).data
        })


class DefaultCategoriesView(APIView):
    """View para criar categorias padrão para novos usuários"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Cria categorias padrão para o usuário"""
        user = request.user
        
        # Verifica se o usuário já tem categorias
        if Category.objects.filter(user=user).exists():
            return Response({
                'message': 'Usuário já possui categorias criadas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Categorias padrão de receita
        income_categories = [
            {'name': 'Salário', 'icon': '💼', 'color': '#4CAF50'},
            {'name': 'Freelance', 'icon': '💻', 'color': '#2196F3'},
            {'name': 'Investimentos', 'icon': '📈', 'color': '#FF9800'},
            {'name': 'Outros', 'icon': '💰', 'color': '#9C27B0'},
        ]
        
        # Categorias padrão de despesa
        expense_categories = [
            {'name': 'Alimentação', 'icon': '🍽️', 'color': '#F44336'},
            {'name': 'Transporte', 'icon': '🚗', 'color': '#FF5722'},
            {'name': 'Moradia', 'icon': '🏠', 'color': '#795548'},
            {'name': 'Saúde', 'icon': '⚕️', 'color': '#E91E63'},
            {'name': 'Entretenimento', 'icon': '🎬', 'color': '#9C27B0'},
            {'name': 'Educação', 'icon': '📚', 'color': '#3F51B5'},
            {'name': 'Outros', 'icon': '💸', 'color': '#607D8B'},
        ]
        
        created_categories = []
        
        # Criar categorias de receita
        for cat_data in income_categories:
            category = Category.objects.create(
                user=user,
                type='income',
                **cat_data
            )
            created_categories.append(category)
        
        # Criar categorias de despesa
        for cat_data in expense_categories:
            category = Category.objects.create(
                user=user,
                type='expense',
                **cat_data
            )
            created_categories.append(category)
        
        serializer = CategorySerializer(created_categories, many=True)
        return Response({
            'message': f'{len(created_categories)} categorias padrão criadas com sucesso',
            'categories': serializer.data
        }, status=status.HTTP_201_CREATED)
