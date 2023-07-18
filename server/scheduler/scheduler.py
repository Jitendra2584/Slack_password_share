from apscheduler.schedulers.background import BackgroundScheduler
from app.models import SecretLink
from django.utils import timezone


def delete_expired_rows():
    current_time = timezone.now()
    expired_rows = SecretLink.objects.filter(expiration_time__lt=current_time)
    print(expired_rows)
    expired_rows.delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_rows, 'interval', minutes=20)
    scheduler.start()

# scheduler = BackgroundScheduler()
# scheduler.add_job(delete_expired_rows, 'interval', seconds=10)
# scheduler.start()
