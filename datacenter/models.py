from datetime import datetime, timedelta

from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    @staticmethod
    def get_duration(visit):
        if not visit.leaved_at:
            return datetime.now().astimezone() - visit.entered_at

        return visit.leaved_at - visit.entered_at

    @staticmethod
    def format_duration(duration):
        return timedelta(seconds=int(duration.total_seconds()))

    @staticmethod
    def is_visit_long(visit, minutes=60):
        duration = Visit.get_duration(visit)
        if duration.total_seconds() // 60 > minutes:
            return True

        return False
