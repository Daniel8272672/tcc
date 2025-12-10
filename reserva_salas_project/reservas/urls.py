from django.urls import path
from . import views
from .views import SalaListView # Importa a classe da nossa nova View

app_name = 'reservas' 

urlpatterns = [
    # Rota para a lista de salas. Esta será a página inicial do app.
    path('', SalaListView.as_view(), name='lista_salas'),
    
    # Próximo passo: Rota para fazer uma reserva em uma sala específica.
    # path('reservar/<int:pk>/', views.ReservaCreateView.as_view(), name='reservar_sala'),
]