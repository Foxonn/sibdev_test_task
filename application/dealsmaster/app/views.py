from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from app import services
from app.exceptions import CsvFileTypeError, CsvFileNeedKeys
from app.serializers import ListDealsSerializer, UploadCsvFileSerializer
from app.models import Person


class UploadFileAPIView(APIView):
    http_method_names = ['post', ]
    parser_classes = (MultiPartParser,)
    serializer_class = UploadCsvFileSerializer

    def post(self, request):
        serializer = UploadCsvFileSerializer(data=request.data)

        try:
            if not serializer.is_valid():
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (CsvFileTypeError, CsvFileNeedKeys, TypeError) as err:
            return Response(
                data={
                    "Status": str(err)
                },
                status=status.HTTP_200_OK
            )
        else:
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
