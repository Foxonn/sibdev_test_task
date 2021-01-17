import csv
import io
from datetime import datetime
from functools import lru_cache

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum, Count
from django.db.models.query import Prefetch

from app.models import Person, Deal, Gem
from app.exceptions import CsvFileTypeError, CsvFileNeedKeys


@lru_cache(maxsize=50)
def get_user_from_cache(customer: str) -> Person:
    return Person.objects.get(username=customer)


@lru_cache(maxsize=50)
def get_gem_from_cache(item: str) -> Gem:
    return Gem.objects.get(named=item)


def get_unique_user(csv_deals: list) -> set:
    if not isinstance(csv_deals, list):
        raise TypeError('`deals` don have type list')

    return set(map(lambda i: i['customer'], csv_deals))


def get_unique_gem(csv_deals: list) -> set:
    if not isinstance(csv_deals, list):
        raise TypeError('`deals` don have type list')

    return set(map(lambda i: i['item'], csv_deals))


def write_deals_to_db(csv_deals: csv.DictReader) -> None:
    """
    :param csv_deals: csv.DictReader
    :return: None
    """
    if not isinstance(csv_deals, csv.DictReader):
        raise TypeError('`deals` don have type csv.DictReader')

    users = []
    gems = []
    deals = []

    get_user_from_cache.cache_clear()
    get_gem_from_cache.cache_clear()

    csv_deals = list(csv_deals)

    unique_user = get_unique_user(csv_deals)
    unique_gem = get_unique_gem(csv_deals)

    for user in unique_user:
        users.append(Person(username=user))

    for gem in unique_gem:
        gems.append(Gem(named=gem))

    Person.objects.bulk_create(users, ignore_conflicts=True)
    Gem.objects.bulk_create(gems, ignore_conflicts=True)

    for deal in csv_deals:
        total = int(deal.get('total'))
        quantity = int(deal.get('quantity'))
        date = validate_datetime_format(deal.get('date'))

        deals.append(
            Deal(
                purchaser=get_user_from_cache(str(deal.get('customer'))),
                item=get_gem_from_cache(str(deal.get('item'))),
                quantity=quantity,
                total=total,
                date=str(date),
            )
        )

    Deal.objects.bulk_create(deals, ignore_conflicts=True)

    return None


def get_best_five_purchasers(queryset):
    purchasers = queryset.annotate(
        spent_money=Sum('deals__total')
    ).order_by('-spent_money')[:5]
    purchasers_ids = list(purchasers.values_list('id', flat=True))

    gems = Gem.objects.filter(
        deals__purchaser__id__in=purchasers_ids
    ).annotate(
        c_deals=Count('deals__purchaser__id', distinct=True)
    ).order_by('-c_deals').filter(c_deals__gte=2)
    gems_ids = list(gems.values_list('id', flat=True))

    purchasers = purchasers.prefetch_related(
        Prefetch(
            'deals',
            Deal.objects.only('item').select_related('item').filter(
                item__id__in=gems_ids
            ),
        )
    )

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

    content_type = ['application/vnd.ms-excel', 'text/csv']
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
        raise CsvFileTypeError()

    if diff := needs_keys.difference(first_row.keys()):
        raise CsvFileNeedKeys(f'Table don`t have column(s): `{diff}`')

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
