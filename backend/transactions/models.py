from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Transaction(models.Model):
    """
    Modelo para transações financeiras (receitas e despesas).
    Core do sistema de controle financeiro.
    """
    TRANSACTION_TYPES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Dinheiro'),
        ('debit_card', 'Cartão de Débito'),
        ('credit_card', 'Cartão de Crédito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('other', 'Outro'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name="Usuário"
    )
    category = models.ForeignKey(
        'categories.Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='transactions',
        verbose_name="Categoria"
    )
    
    # Dados da transação
    description = models.CharField(max_length=200, verbose_name="Descrição")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor"
    )
    type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES,
        verbose_name="Tipo"
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS,
        default='cash',
        verbose_name="Método de Pagamento"
    )
    
    # Datas
    date = models.DateField(verbose_name="Data da Transação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    # Campos opcionais
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Tags separadas por vírgula",
        verbose_name="Tags"
    )
    
    # Campos para transações recorrentes (futuro)
    is_recurring = models.BooleanField(default=False, verbose_name="Recorrente")
    recurring_frequency = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        choices=[
            ('daily', 'Diário'),
            ('weekly', 'Semanal'),
            ('monthly', 'Mensal'),
            ('yearly', 'Anual'),
        ],
        verbose_name="Frequência de Recorrência"
    )
    
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.description} - {self.get_type_display()}: R$ {self.amount}"
    
    def save(self, *args, **kwargs):
        # Validação: categoria deve ser do mesmo tipo da transação
        if self.category and self.category.type != self.type:
            raise ValueError("Tipo da categoria deve corresponder ao tipo da transação")
        super().save(*args, **kwargs)
    
    @property
    def formatted_amount(self):
        """Retorna o valor formatado em reais"""
        return f"R$ {self.amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_tags_list(self):
        """Retorna as tags como uma lista"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
