import csv
import io
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum, Count

from .models import Person, Deal, Gem


def get_best_five_purchasers(queryset):

    purchasers = queryset.annotate(
        sell__count=Count('deals__item__id')
    ).filter(sell__count__gte=2).annotate(
        spent_money=Sum('deals__total')
    ).order_by('-spent_money')[:5]

    return purchasers


def validate_upload_csv(file: InMemoryUploadedFile) -> None:
    """
    :param file: InMemoryUploadedFile
    :return: None
    """

    if not isinstance(file, InMemoryUploadedFile):
        raise TypeError(
            f'`file` have type {type(file)}, must have InMemoryUploadedFile'
        )

    content_type = ['application/vnd.ms-excel']
    allow_extension = ['csv']

    file_content_type = file.content_type
    file_name, file_extension = str(file._name).rsplit('.', maxsplit=1)

    if file_extension not in allow_extension:
        raise TypeError(
            'file have wrong extension: `%s`, expect %s' % (
                file_extension, allow_extension
            )
        )

    if file_content_type not in content_type:
        raise TypeError(
            'file have wrong content_type: `%s`, expect %s' % (
                file_content_type, content_type
            )
        )

    return None


def validate_datetime_format(date: str) -> datetime:
    """
    :param date: str
    :return: datetime
    """
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')


def validate_column_deals(deals: csv.DictReader) -> None:
    """
    :param deals: csv.DictReader
    :return: None
    """

    if not isinstance(deals, csv.DictReader):
        raise TypeError('`deals` don have type csv.DictReader')

    needs_keys = {'customer', 'item', 'total', 'quantity', 'date'}
    first_row = next(deals, None)

    if not first_row:
        raise Exception('file don`t have data')

    if diff := needs_keys.difference(first_row.keys()):
        raise Exception(f'table don`t have column(s): `{diff}`')

    return None


def write_deals_to_db(deals: csv.DictReader) -> None:
    """
    :param deals: csv.DictReader
    :return: None
    """
    if not isinstance(deals, csv.DictReader):
        raise TypeError('`deals` don have type csv.DictReader')

    for deal in deals:
        person, _ = Person.objects.get_or_create(
            username=deal.get('customer')
        )

        total = int(deal.get('total'))
        quantity = int(deal.get('quantity'))
        date = validate_datetime_format(deal.get('date'))

        gem, _ = Gem.objects.get_or_create(
            named=deal.get('item'),
        )

        Deal.objects.get_or_create(
            purchaser=person,
            item=gem,
            quantity=quantity,
            total=total,
            date=str(date),
        )
    return None


def parse_csv_file(file: InMemoryUploadedFile) -> csv.DictReader:
    """
    :param file: InMemoryUploadedFile
    :return: csv.DictReader
    """
    if not isinstance(file, InMemoryUploadedFile):
        raise TypeError(
            f'`file` have type {type(file)}, must have InMemoryUploadedFile'
        )

    validate_upload_csv(file)
    decode_file = file.read().decode()
    io_string = io.StringIO(decode_file)
    reader = csv.DictReader(io_string, delimiter=',')

    return reader
