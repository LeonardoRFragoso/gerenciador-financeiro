from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuário customizado para o sistema de controle financeiro.
    Estende o modelo padrão do Django com campos específicos para finanças.
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, verbose_name="Nome")
    last_name = models.CharField(max_length=30, verbose_name="Sobrenome")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    
    # Configurações financeiras
    monthly_income = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Renda Mensal"
    )
    currency = models.CharField(
        max_length=3, 
        default='BRL',
        verbose_name="Moeda"
    )
    
    # Configurações de notificação
    email_notifications = models.BooleanField(default=True, verbose_name="Notificações por Email")
    push_notifications = models.BooleanField(default=True, verbose_name="Notificações Push")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_total_balance(self):
        """Calcula o saldo total do usuário baseado nas transações"""
        from transactions.models import Transaction
        
        income = Transaction.objects.filter(
            user=self, 
            type='income'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        expenses = Transaction.objects.filter(
            user=self, 
            type='expense'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        return income - expenses
