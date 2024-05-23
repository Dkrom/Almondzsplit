from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Split, Balance
from .serializers import UserSerializer, SplitSerializer, BalanceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SplitViewSet(viewsets.ModelViewSet):
    queryset = Split.objects.all()
    serializer_class = SplitSerializer

    @action(detail=True, methods=['post'])
    def add_split(self, request, pk=None):
        split = self.get_object()
        split_type = split.split_type
        participants = split.participants.all()
        amount = split.amount
        paid_by = split.paid_by

        if split_type == 'EQUALLY':
            split_amount = amount / len(participants)
            for participant in participants:
                if participant != paid_by:
                    self.update_balance(paid_by, participant, split_amount)
        elif split_type == 'EXACT':
            for participant, split_amount in zip(participants, split.split_values):
                if participant != paid_by:
                    self.update_balance(paid_by, participant, split_amount)
        elif split_type == 'PERCENTAGE':
            for participant, percentage in zip(participants, split.split_values):
                if participant != paid_by:
                    split_amount = amount * (percentage / 100)
                    self.update_balance(paid_by, participant, split_amount)

        return Response({'status': 'split added'})

class BalanceView(APIView):
    def get(self, request, user_id):
        balances = Balance.objects.filter(user_id=user_id)
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
