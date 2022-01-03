from django.db import models

class LoggerKey(models.Model):
    username = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    settings = models.TextField()

    class Meta:
        managed = True
        db_table = 'user_key'


class Event(models.Model):
    timestamp = models.DateTimeField()
    logger_key = models.ForeignKey(LoggerKey, models.DO_NOTHING, db_column='logger_key_id')
    event_type = models.IntegerField(default=0)  # 0 = keyboard only, 1 = keyboard + process
    content = models.TextField()

    class Meta:
        managed = True
        db_table = 'event'
        unique_together = (('timestamp', 'logger_key_id'),)
