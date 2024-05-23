from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Split, SplitParticipant, Balance
from .serializers import UserSerializer, SplitSerializer, SplitParticipantSerializer, BalanceSerializer

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id='U1', name='dravid', email='dravid@example.com', mobile='1234567890')

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'dravid')
        self.assertEqual(self.user.email, 'dravid@example.com')

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'dravid')
        self.assertEqual(serializer.data['email'], 'dravid@example.com')

class SplitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id='U1', name='dravid', email='dravid@example.com', mobile='1234567890')
        self.split = Split.objects.create(paid_by=self.user, amount=100.00, split_type='EQUALLY')

    def test_split_creation(self):
        self.assertEqual(self.split.paid_by.name, 'dravid')
        self.assertEqual(self.split.amount, 100.00)
        self.assertEqual(self.split.split_type, 'EQUALLY')

    def test_split_serializer(self):
        serializer = SplitSerializer(self.split)
        self.assertEqual(serializer.data['amount'], '100.00')
        self.assertEqual(serializer.data['split_type'], 'EQUALLY')

class SplitParticipantTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(user_id='U1', name='dravid', email='dravid@example.com', mobile='1234567890')
        self.user2 = User.objects.create(user_id='U2', name='shivam', email='shivam@example.com', mobile='0987654321')
        self.split = Split.objects.create(paid_by=self.user1, amount=100.00, split_type='EQUALLY')
        self.split_participant = SplitParticipant.objects.create(split=self.split, user=self.user2, share=50.00)

    def test_split_participant_creation(self):
        self.assertEqual(self.split_participant.split, self.split)
        self.assertEqual(self.split_participant.user, self.user2)
        self.assertEqual(self.split_participant.share, 50.00)

    def test_split_participant_serializer(self):
        serializer = SplitParticipantSerializer(self.split_participant)
        self.assertEqual(serializer.data['share'], '50.00')
        self.assertEqual(serializer.data['user'], self.user2.id)

class BalanceTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(user_id='U1', name='dravid', email='dravid@example.com', mobile='1234567890')
        self.user2 = User.objects.create(user_id='U2', name='shivam', email='shivam@example.com', mobile='0987654321')
        self.balance = Balance.objects.create(user=self.user1, owes_to=self.user2, amount=50.00)

    def test_balance_creation(self):
        self.assertEqual(self.balance.user, self.user1)
        self.assertEqual(self.balance.owes_to, self.user2)
        self.assertEqual(self.balance.amount, 50.00)

    def test_balance_serializer(self):
        serializer = BalanceSerializer(self.balance)
        self.assertEqual(serializer.data['amount'], 50.00)
        self.assertEqual(serializer.data['user'], self.user1.id)

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(user_id='U1', name='dravid', email='dravid@example.com', mobile='1234567890')
        self.user2 = User.objects.create(user_id='U2', name='shivam', email='shivam@example.com', mobile='0987654321')

    def test_user_api(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_split_api(self):
        split = Split.objects.create(paid_by=self.user1, amount=100.00, split_type='EQUALLY')
        response = self.client.get('/splits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
