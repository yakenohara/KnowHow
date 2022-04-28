from django.db import models

from rest_framework.authtoken.models import Token

from common.utilities import StrChoiceEnum

# Create your models here.

class TokenForRESTAPI(Token):
    
    expired_date = models.DateTimeField(verbose_name = '有効期限', null = True, blank = True)

    class Expiration(StrChoiceEnum):
        ONE_WEEK = ('7 days', '1 週間')
        ONE_MONTH = ('30 days', '1 ヶ月間')
        THREE_MONTHS = ('90 days', '3 ヶ月間')
        NO_EXPIRATION = ('no expiration', '有効期限なし')

    expiration = models.CharField(verbose_name = '設定有効期限', max_length = 16, choices = Expiration.choices(), null = True)
