from django.test import TestCase
from django.contrib.auth.models import User
from .models import Sala, Recurso, Reserva
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class SalaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sala = Sala.objects.create(
            nome="Sala Azul",
            capacidade=10,
            localizacao="Prédio A"
        )

    def test_criacao_sala(self):
        self.assertEqual(self.sala.nome, "Sala Azul")
        self.assertEqual(self.sala.capacidade, 10)
        self.assertEqual(self.sala.localizacao, "Prédio A")

    def test_status_padrao_disponivel(self):
        self.assertTrue(self.sala.disponivel)  # valor default=True

    def test_str_da_sala(self):
        self.assertEqual(str(self.sala), "Sala Azul")


class RecursoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sala = Sala.objects.create(nome="Sala Verde", capacidade=8)
        cls.recurso = Recurso.objects.create(
            nome="Projetor",
            descricao="Projetor Full HD"
        )
        cls.recurso.salas.add(cls.sala)

    def test_criacao_recurso(self):
        self.assertEqual(self.recurso.nome, "Projetor")
        self.assertEqual(self.recurso.descricao, "Projetor Full HD")

    def test_relacionamento_sala_recurso(self):
        self.assertIn(self.sala, self.recurso.salas.all())

    def test_str_do_recurso(self):
        self.assertEqual(str(self.recurso), "Projetor")


class ReservaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="joao",
            password="senha123"
        )

        cls.sala = Sala.objects.create(
            nome="Sala Amarela",
            capacidade=5
        )

        cls.data_inicio = make_aware(datetime.now())
        cls.data_fim = cls.data_inicio + timedelta(hours=1)

        cls.reserva = Reserva.objects.create(
            sala=cls.sala,
            funcionario=cls.user,
            data_inicio=cls.data_inicio,
            data_fim=cls.data_fim,
            objetivo="Reunião de planejamento"
        )

    def test_criacao_reserva(self):
        self.assertEqual(self.reserva.sala.nome, "Sala Amarela")
        self.assertEqual(self.reserva.funcionario.username, "joao")
        self.assertEqual(self.reserva.objetivo, "Reunião de planejamento")

    def test_status_padrao_e_pendente(self):
        self.assertEqual(self.reserva.status, "PENDENTE")

    def test_datas_da_reserva(self):
        self.assertIsNotNone(self.reserva.data_inicio)
        self.assertIsNotNone(self.reserva.data_fim)
        self.assertTrue(self.reserva.data_fim > self.reserva.data_inicio)

    def test_str_da_reserva(self):
        texto = str(self.reserva)
        self.assertIn("Reserva de Sala Amarela", texto)
        self.assertIn("por joao", texto)
