from django.db import models

class LoggerKey(models.Model):
    username = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    settings = models.TextField()

    class Meta:
        managed = True
        db_table = 'logger_key'


class Event(models.Model):
    timestamp = models.DateTimeField()
    logger_key = models.ForeignKey(LoggerKey, models.DO_NOTHING, db_column='logger_key_id')
    content = models.TextField(default="")
    processes = models.TextField(default="")

    class Meta:
        managed = True
        db_table = 'event'
        unique_together = (('timestamp', 'logger_key_id'),)
