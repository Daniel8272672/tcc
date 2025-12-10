from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Sala, Reserva
from datetime import datetime

# =======================================================
# 1. VISUALIZAÇÃO DE SALAS (FUNCIONÁRIO)
# =======================================================

class SalaListView(LoginRequiredMixin, ListView):
    """
    Lista todas as salas disponíveis. 
    Apenas usuários logados (Funcionários e Admin) podem acessar.
    """
    model = Sala
    template_name = 'reservas/sala_list.html'
    context_object_name = 'salas'
    
    # O LoginRequiredMixin redireciona para a página de login se o usuário não estiver autenticado.
    login_url = reverse_lazy('login') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Você pode adicionar lógica aqui para verificar a próxima reserva, se desejar.
        return context

# Em seguida, você criaria outras views como:
# class ReservaCreateView(LoginRequiredMixin, CreateView): ...