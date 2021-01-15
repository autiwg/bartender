from django.utils import timezone
from django.utils.text import slugify


def generate_billed_document_path(instance, filename):
    cur_time = timezone.now()

    return f"{cur_time.strftime('%Y/%m')}/{slugify(instance.name)}-{cur_time.strftime('%d.%m.%Y %H:%M')}.csv"
