from django.db import models
from django.db.models import F

from restaurant.models import Restaurant
from django.contrib.auth.models import User


class BookMark(models.Model):
    """
    ForeignKey
    - Restaurant id(PK)
    - User id(PK)
    """
    # , 필요 없음
    # related_name 같은 내용이라 필요 없음
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    # 변수이름 수정 필요, default/null=False 의미가 맞지 않음
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')

    # bookmarks = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=False, related_name='bookmarks',
    #                               unique=True)
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Race Condition 방지 코드 필요
        # https://docs.djangoproject.com/en/3.0/ref/models/expressions/#avoiding-race-conditions-using-f
        # https://docs.djangoproject.com/en/3.0/ref/models/expressions/#f-expressions
        Restaurant.objects.filter(id=self.restaurant_id).update(rest_count=F('rest_count') + 1)
        super().save()

    # convention 맞지 않음
    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'restaurant']
