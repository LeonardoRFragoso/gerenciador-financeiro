from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Goal(models.Model):
    """
    Modelo para metas financeiras dos usuários.
    Permite definir objetivos de economia e acompanhar progresso.
    """
    GOAL_CATEGORIES = [
        ('emergency', 'Reserva de Emergência'),
        ('vacation', 'Viagem/Férias'),
        ('house', 'Casa/Imóvel'),
        ('car', 'Veículo'),
        ('education', 'Educação'),
        ('investment', 'Investimento'),
        ('debt', 'Quitação de Dívida'),
        ('other', 'Outro'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('completed', 'Concluída'),
        ('paused', 'Pausada'),
        ('cancelled', 'Cancelada'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='goals',
        verbose_name="Usuário"
    )
    
    # Informações básicas da meta
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    category = models.CharField(
        max_length=20, 
        choices=GOAL_CATEGORIES,
        verbose_name="Categoria"
    )
    
    # Valores financeiros
    target_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Objetivo"
    )
    current_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Atual"
    )
    
    # Datas e prazos
    target_date = models.DateField(verbose_name="Data Objetivo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Concluído em")
    
    # Status e prioridade
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Status"
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_LEVELS,
        default='medium',
        verbose_name="Prioridade"
    )
    
    # Configurações
    is_public = models.BooleanField(default=False, verbose_name="Meta Pública")
    auto_save = models.BooleanField(default=False, verbose_name="Economia Automática")
    monthly_contribution = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Contribuição Mensal"
    )
    
    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Metas"
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'target_date']),
            models.Index(fields=['user', 'priority']),
        ]
    
    def __str__(self):
        return f"{self.title} - R$ {self.target_amount}"
    
    @property
    def progress_percentage(self):
        """Calcula a porcentagem de progresso da meta"""
        if self.target_amount > 0:
            return min((self.current_amount / self.target_amount) * 100, 100)
        return 0
    
    @property
    def remaining_amount(self):
        """Calcula o valor restante para atingir a meta"""
        return max(self.target_amount - self.current_amount, 0)
    
    @property
    def is_completed(self):
        """Verifica se a meta foi atingida"""
        return self.current_amount >= self.target_amount
    
    @property
    def days_remaining(self):
        """Calcula quantos dias restam para a data objetivo"""
        from datetime import date
        if self.target_date:
            delta = self.target_date - date.today()
            return max(delta.days, 0)
        return None
    
    def add_contribution(self, amount):
        """Adiciona uma contribuição à meta"""
        self.current_amount += Decimal(str(amount))
        if self.is_completed and self.status == 'active':
            self.status = 'completed'
            from django.utils import timezone
            self.completed_at = timezone.now()
        self.save()
    
    def get_monthly_target(self):
        """Calcula quanto deve ser economizado por mês para atingir a meta"""
        if self.days_remaining and self.days_remaining > 0:
            months_remaining = max(self.days_remaining / 30, 1)
            return self.remaining_amount / Decimal(str(months_remaining))
        return self.remaining_amount
