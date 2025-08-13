from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Modelo para categorias de transações financeiras.
    Permite categorização personalizada por usuário.
    """
    TRANSACTION_TYPES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES,
        verbose_name="Tipo de Transação"
    )
    color = models.CharField(
        max_length=7, 
        default='#FFD700',
        help_text="Cor em formato hexadecimal (ex: #FFD700)",
        verbose_name="Cor"
    )
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Emoji ou ícone para representar a categoria",
        verbose_name="Ícone"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='categories',
        verbose_name="Usuário"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['type', 'name']
        unique_together = ['user', 'name', 'type']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    def get_transaction_count(self):
        """Retorna o número de transações desta categoria"""
        return self.transactions.count()
    
    def get_total_amount(self):
        """Retorna o valor total das transações desta categoria"""
        return self.transactions.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
