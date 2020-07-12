from django.db import models


class Restaurant(models.Model):
    # null=False 이어야 할거 같음
    # TextField 필요 없음
    rest_name = models.CharField(max_length=30, default=None, help_text='식당 이름')
    # 별점
    rest_star = models.FloatField(null=True, default=None)
    # 주소
    rest_address = models.CharField(max_length=50, default=None)
    # 전화번호
    rest_phone_number = models.CharField(max_length=30, null=True, default=None)
    # 음식 종류
    rest_food = models.CharField(max_length=30, null=True, default=None)
    # 가격
    rest_sale = models.CharField(max_length=20, null=True, default=None)
    # 영업 시간
    rest_time = models.CharField(max_length=10, null=True, default=None)
    # 쉬는 시간
    rest_break_time = models.CharField(max_length=10, null=True, default=None)
    # 북마크 개수
    # PositiveInt
    rest_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.rest_name
