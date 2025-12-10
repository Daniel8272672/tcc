from django.db import models
# Importa o modelo de usuário padrão do Django (para Admin/Funcionário)
from django.contrib.auth.models import User 

class Sala(models.Model):
    """
    Modelo Principal: Sala
    Representa a sala que pode ser reservada.
    """
    nome = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nome da Sala"
    )
    capacidade = models.PositiveIntegerField(
        default=1, 
        verbose_name="Capacidade Máxima"
    )
    localizacao = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Localização/Prédio"
    )
    
    # Adicione um campo para status (opcionalmente)
    disponivel = models.BooleanField(
        default=True, 
        verbose_name="Em Uso/Disponível"
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Sala de Reunião"
        verbose_name_plural = "Salas de Reunião"


class Recurso(models.Model):
    """
    Modelo Principal: Recurso
    Itens que uma sala pode ter (Projetor, Lousa, Videoconferência, etc.)
    """
    nome = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Nome do Recurso"
    )
    descricao = models.TextField(
        blank=True, 
        null=True
    )
    
    # Relacionamento N-N (Muitos para Muitos): Uma Sala tem Vários Recursos, 
    # e um Recurso está presente em Várias Salas.
    salas = models.ManyToManyField(
        Sala, 
        related_name='recursos', 
        verbose_name="Salas com este Recurso"
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Recurso da Sala"
        verbose_name_plural = "Recursos das Salas"


class Reserva(models.Model):
    """
    Modelo Principal: Reserva
    Representa o agendamento de uma sala por um funcionário.
    """
    
    # Status possíveis da reserva
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    # Relacionamento N-1 (Muitos para Um): Muitas Reservas para Uma Sala.
    sala = models.ForeignKey(
        Sala, 
        on_delete=models.CASCADE, 
        related_name='reservas_sala'
    )
    
    # Relacionamento N-1 (Muitos para Um): Muitas Reservas para Um Funcionário (User).
    # O Funcionário é o User padrão do Django.
    funcionario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='minhas_reservas', 
        verbose_name="Funcionário/Usuário"
    )
    
    data_inicio = models.DateTimeField(
        verbose_name="Início da Reserva"
    )
    data_fim = models.DateTimeField(
        verbose_name="Fim da Reserva"
    )
    
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PENDENTE'
    )
    
    # Campo para justificar a reserva (opcional)
    objetivo = models.TextField(
        verbose_name="Objetivo da Reunião"
    )

    def __str__(self):
        data = self.data_inicio.strftime("%d/%m/%Y às %H:%M")
        return f"Reserva de {self.sala.nome} por {self.funcionario.username} em {data}"

    class Meta:
        ordering = ['data_inicio']
        verbose_name = "Reserva de Sala"
        verbose_name_plural = "Reservas de Salas"