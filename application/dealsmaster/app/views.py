from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from . import services
from .serializers import ListDealsSerializer
from .models import Person


class UploadFileViewSet(APIView):
    http_method_names = ['post', ]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            up_file = request.FILES['deals']
            deals = services.parse_csv_file(up_file)
            services.validate_column_deals(deals)
            services.write_deals_to_db(deals)
        except Exception as err:
            msg = "в процессе обработки файла произошла ошибка."
            raise APIException(
                {"Status": "Error, Desc: %s - %s" % (ascii(err), msg)}
            )

        return Response(
            data={
                'Status': 'Ok',
            },
            status=status.HTTP_201_CREATED
        )


class ListDealsView(generics.ListAPIView):
    http_method_names = ['get', ]
    queryset = Person.objects.all()
    serializer_class = ListDealsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return services.get_best_five_purchasers(queryset)
