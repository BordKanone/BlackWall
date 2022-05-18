from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import ClientPurse, QueueClientTransactions, Transactions


class ClientPurseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    client = serializers.ReadOnlyField(source='client__user')

    def create(self, validated_data):
        client = User.objects.create(
            username=validated_data['name'],
            password=make_password(validated_data['password'])
        )

        queue = validated_data.pop('queue')

        client = ClientPurse.objects.create(
            client=client,
            name=validated_data['name'],
            purse_number=validated_data['purse_number'],
            balance=validated_data['balance'],
        )
        client.queue.add(*queue)

        return client

    class Meta:
        model = ClientPurse
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


class QueueTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueueClientTransactions
        fields = '__all__'
