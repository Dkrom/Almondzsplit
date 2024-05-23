from rest_framework import serializers
from .models import User, Split, SplitParticipant, Balance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = '__all__'

class SplitParticipantSerializer(serializers.ModelSerializer):
    split = serializers.PrimaryKeyRelatedField(queryset=Split.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SplitParticipant
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owes_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Balance
        fields = '__all__'
