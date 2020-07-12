from rest_framework import serializers, status
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from restaurant.serializer import RestSerializer
from .models import BookMark


class CustomUniqueTogetherValidator(UniqueTogetherValidator):
    #
    def enforce_required_fields(self, attrs, serializer):
        attrs['user'] = serializer.context['request'].user
        super().enforce_required_fields(attrs, serializer)


class BookMarkSerializer(serializers.ModelSerializer):
    """ list: user_id, restaurant_id Serializer"""

    class Meta:
        model = BookMark
        fields = (
            'id',
            'restaurant',
            'user',
        )
        # 모델에서 트랜잭션 에러가 발생하기때문에 시리얼라이저에서 먼저 검사해야한다 -> 400에러도 발생함 !
        # validate할 때 user 데이터가 없어서 에러 발생 -> enforce_required_fields를 오버라이드해서 user와 함께 검사!
        validators = [
            CustomUniqueTogetherValidator(
                queryset=BookMark.objects.all(),
                fields=('restaurant', 'user')
            )
        ]


class UserBookMarkSerializer(serializers.ModelSerializer):
    """ 식당 정보 Serializer"""
    restaurant = RestSerializer(read_only=True)

    class Meta:
        model = BookMark
        fields = (
            'restaurant',
        )
