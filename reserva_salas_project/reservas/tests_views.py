from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reservas.models import Sala

class SalaListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Criar usuário para login
        cls.user = User.objects.create_user(
            username='funcionario',
            password='123456'
        )

        # Criar salas
        cls.sala1 = Sala.objects.create(
            nome="Sala Azul",
            capacidade=10,
            localizacao="Prédio A"
        )
        cls.sala2 = Sala.objects.create(
            nome="Sala Vermelha",
            capacidade=20,
            localizacao="Prédio B"
        )

    def test_redireciona_se_nao_estiver_logado(self):
        url = reverse('sala_list')  # ajuste este nome para o nome REAL da sua rota
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirecionamento
        self.assertIn("/login", response.url)  # garante que redireciona pro login

    def test_listagem_salas_usuario_logado(self):
        self.client.login(username='funcionario', password='123456')
        url = reverse('sala_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas/sala_list.html')
        self.assertContains(response, 'Sala Azul')
        self.assertContains(response, 'Sala Vermelha')

    def test_contexto_da_view(self):
        self.client.login(username='funcionario', password='123456')
        url = reverse('sala_list')
        response = self.client.get(url)

        salas = response.context['salas']
        self.assertEqual(len(salas), 2)
        self.assertIn(self.sala1, salas)
        self.assertIn(self.sala2, salas)
