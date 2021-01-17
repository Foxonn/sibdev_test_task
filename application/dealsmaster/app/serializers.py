from rest_framework import serializers

from app import services
from app.models import Person, Gem, Deal


class UploadCsvFileSerializer(serializers.Serializer):
    deals = serializers.FileField()

    def validate(self, data):
        up_file = data['deals']
        deals = services.parse_csv_file(up_file)
        services.validate_column_deals(deals)
        services.write_deals_to_db(deals)

        return data


class GemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = ('named',)


class DealsSerializer(serializers.ModelSerializer):
    item = GemsSerializer(read_only=True, )

    class Meta:
        model = Deal
        fields = ('item',)


class ListDealsSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField(read_only=True, )
    deals = serializers.SerializerMethodField('get_deals')

    def get_deals(self, person):
        qs = person.deals.all().distinct('item__named')
        serializer = DealsSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Person
        fields = ('id', 'username', 'spent_money', 'deals')
