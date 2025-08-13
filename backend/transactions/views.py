from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction
from .serializers import (
    TransactionSerializer, 
    TransactionCreateSerializer, 
    TransactionSummarySerializer
)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de transações"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['type', 'category', 'payment_method', 'date']
    search_fields = ['description', 'notes', 'tags']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        # Usuários só veem suas próprias transações
        return Transaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retorna as transações mais recentes"""
        limit = int(request.query_params.get('limit', 10))
        transactions = self.get_queryset()[:limit]
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Retorna transações agrupadas por categoria"""
        queryset = self.get_queryset()
        
        # Agrupar por categoria
        categories_data = {}
        for transaction in queryset:
            category_name = transaction.category.name if transaction.category else 'Sem categoria'
            if category_name not in categories_data:
                categories_data[category_name] = {
                    'category': category_name,
                    'transactions': [],
                    'total_amount': 0,
                    'count': 0
                }
            
            categories_data[category_name]['transactions'].append(
                TransactionSerializer(transaction).data
            )
            categories_data[category_name]['total_amount'] += float(transaction.amount)
            categories_data[category_name]['count'] += 1
        
        return Response(list(categories_data.values()))


class TransactionSummaryView(APIView):
    """View para resumo financeiro"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Retorna resumo financeiro do usuário"""
        user = request.user
        
        # Parâmetros de período
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Se não especificado, usar mês atual
        if not start_date or not end_date:
            now = timezone.now()
            start_date = now.replace(day=1).date()
            end_date = (start_date.replace(month=start_date.month + 1) - timedelta(days=1))
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Filtrar transações do período
        transactions = Transaction.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        )
        
        # Calcular totais
        income_total = transactions.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense_total = transactions.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Contar transações
        total_count = transactions.count()
        income_count = transactions.filter(type='income').count()
        expense_count = transactions.filter(type='expense').count()
        
        summary_data = {
            'total_income': income_total,
            'total_expenses': expense_total,
            'balance': income_total - expense_total,
            'transaction_count': total_count,
            'income_count': income_count,
            'expense_count': expense_count,
            'period_start': start_date,
            'period_end': end_date
        }
        
        serializer = TransactionSummarySerializer(summary_data)
        return Response(serializer.data)


class MonthlyReportView(APIView):
    """View para relatório mensal"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Retorna dados para gráfico mensal"""
        user = request.user
        
        # Últimos 12 meses
        end_date = timezone.now().date()
        start_date = end_date.replace(month=1) if end_date.month == 12 else end_date.replace(year=end_date.year-1, month=end_date.month+1)
        
        monthly_data = []
        current_date = start_date
        
        while current_date <= end_date:
            # Primeiro e último dia do mês
            month_start = current_date.replace(day=1)
            if current_date.month == 12:
                month_end = current_date.replace(year=current_date.year+1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = current_date.replace(month=current_date.month+1, day=1) - timedelta(days=1)
            
            # Transações do mês
            month_transactions = Transaction.objects.filter(
                user=user,
                date__range=[month_start, month_end]
            )
            
            income = month_transactions.filter(type='income').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            expenses = month_transactions.filter(type='expense').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            monthly_data.append({
                'month': current_date.strftime('%Y-%m'),
                'month_name': current_date.strftime('%B %Y'),
                'income': float(income),
                'expenses': float(expenses),
                'balance': float(income - expenses)
            })
            
            # Próximo mês
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year+1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month+1)
        
        return Response(monthly_data)


class CategoriesReportView(APIView):
    """View para relatório por categorias"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Retorna gastos por categoria"""
        user = request.user
        transaction_type = request.query_params.get('type', 'expense')
        
        # Agrupar por categoria
        from categories.models import Category
        categories = Category.objects.filter(user=user, type=transaction_type)
        
        categories_data = []
        for category in categories:
            total = category.transactions.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            categories_data.append({
                'category': category.name,
                'color': category.color,
                'icon': category.icon,
                'total': float(total),
                'percentage': 0  # Será calculado no frontend
            })
        
        # Ordenar por valor
        categories_data.sort(key=lambda x: x['total'], reverse=True)
        
        return Response(categories_data)
