from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Count
from .models import Goal
from .serializers import (
    GoalSerializer, 
    GoalCreateSerializer, 
    GoalContributionSerializer,
    GoalSummarySerializer
)


class GoalViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de metas"""
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['target_date', 'priority', 'created_at', 'progress_percentage']
    ordering = ['-priority', 'target_date']
    
    def get_queryset(self):
        # Usuários só veem suas próprias metas
        return Goal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GoalCreateSerializer
        return GoalSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retorna apenas metas ativas"""
        active_goals = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(active_goals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Retorna metas concluídas"""
        completed_goals = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(completed_goals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """Retorna metas agrupadas por prioridade"""
        queryset = self.get_queryset().filter(status='active')
        
        priorities = {
            'urgent': queryset.filter(priority='urgent'),
            'high': queryset.filter(priority='high'),
            'medium': queryset.filter(priority='medium'),
            'low': queryset.filter(priority='low'),
        }
        
        result = {}
        for priority, goals in priorities.items():
            result[priority] = GoalSerializer(goals, many=True).data
        
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Alterna status da meta (ativa/pausada)"""
        goal = self.get_object()
        
        if goal.status == 'active':
            goal.status = 'paused'
        elif goal.status == 'paused':
            goal.status = 'active'
        else:
            return Response({
                'error': 'Não é possível alterar status de metas concluídas ou canceladas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        goal.save()
        serializer = self.get_serializer(goal)
        return Response(serializer.data)


class GoalSummaryView(APIView):
    """View para resumo de metas"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Retorna resumo das metas do usuário"""
        user = request.user
        goals = Goal.objects.filter(user=user)
        
        # Contadores básicos
        total_goals = goals.count()
        active_goals = goals.filter(status='active').count()
        completed_goals = goals.filter(status='completed').count()
        
        # Valores totais
        total_target = goals.aggregate(Sum('target_amount'))['target_amount__sum'] or 0
        total_current = goals.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
        total_remaining = total_target - total_current
        
        # Progresso médio
        active_goals_queryset = goals.filter(status='active')
        if active_goals_queryset.exists():
            average_progress = sum([goal.progress_percentage for goal in active_goals_queryset]) / active_goals_queryset.count()
        else:
            average_progress = 0
        
        # Metas por prioridade
        goals_by_priority = {}
        for priority in ['urgent', 'high', 'medium', 'low']:
            count = goals.filter(priority=priority, status='active').count()
            goals_by_priority[priority] = count
        
        # Metas por categoria
        goals_by_category = {}
        for category in Goal.GOAL_CATEGORIES:
            count = goals.filter(category=category[0], status='active').count()
            if count > 0:
                goals_by_category[category[1]] = count
        
        summary_data = {
            'total_goals': total_goals,
            'active_goals': active_goals,
            'completed_goals': completed_goals,
            'total_target_amount': total_target,
            'total_current_amount': total_current,
            'total_remaining_amount': total_remaining,
            'average_progress': average_progress,
            'goals_by_priority': goals_by_priority,
            'goals_by_category': goals_by_category
        }
        
        serializer = GoalSummarySerializer(summary_data)
        return Response(serializer.data)


class GoalContributionView(APIView):
    """View para adicionar contribuições às metas"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, goal_id):
        """Adiciona uma contribuição à meta"""
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        
        if goal.status != 'active':
            return Response({
                'error': 'Só é possível contribuir para metas ativas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GoalContributionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data.get('description', '')
            
            # Adicionar contribuição
            goal.add_contribution(amount)
            
            # Criar registro da transação (opcional - pode ser implementado depois)
            # Transaction.objects.create(
            #     user=request.user,
            #     description=f"Contribuição para meta: {goal.title}",
            #     amount=amount,
            #     type='expense',
            #     date=timezone.now().date()
            # )
            
            # Retornar meta atualizada
            goal_serializer = GoalSerializer(goal)
            return Response({
                'message': f'Contribuição de R$ {amount} adicionada com sucesso',
                'goal': goal_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
