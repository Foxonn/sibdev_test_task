from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Person, Gem, Deal


class GemsSerializer(ModelSerializer):
    class Meta:
        model = Gem
        fields = ('named',)


class DealsSerializer(ModelSerializer):
    item = GemsSerializer()

    class Meta:
        model = Deal
        fields = ('item',)


class ListDealsSerializer(ModelSerializer):
    spent_money = IntegerField()
    deals = DealsSerializer(many=True)

    class Meta:
        model = Person
        fields = ('id', 'username', 'spent_money', 'deals')
