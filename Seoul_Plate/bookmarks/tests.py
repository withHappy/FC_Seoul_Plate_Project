from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from bookmarks.models import BookMark
from restaurant.models import Restaurant


class BookMarkTestCode(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='adasd',
            password='12345'
        )
        self.users = baker.make('auth.User', _quantity=4)

        # self.restaurant = Restaurant.objects.create()

        self.test_restaurant = Restaurant.objects.create(rest_name='abcmarket', rest_star=2.9, rest_address='seoul')
        Restaurant.objects.create(rest_name='endmarket', rest_star=5.0, rest_address='busan')
        self.query_set = Restaurant.objects.all()

    def test_bookmark_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'restaurant': self.test_restaurant.id
        }

        response = self.client.post('/api/bookmark', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['id'])
        self.assertEqual(response.data['restaurant'], data['restaurant'])

    def test_bookmark_delete(self):
        self.client.force_authenticate(user=self.user)
        test_bookmark = BookMark.objects.create(user=self.user, restaurant=self.test_restaurant)
        entry = BookMark.objects.get(id=test_bookmark.id)

        response = self.client.delete(f'/api/bookmark/{test_bookmark.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(BookMark.objects.filter(id=entry.id).exists())

    def test_bookmark_duplicate(self):
        self.client.force_authenticate(user=self.user)
        baker.make('bookmarks.BookMark', user=self.user, restaurant_id=self.test_restaurant.id)

        data = {
            'restaurant': self.test_restaurant.id
        }
        response = self.client.post('/api/bookmark', data=data)

        self.assertEqual(BookMark.objects.filter(
            restaurant=data['restaurant'],
            user=self.user,
        ).count(), 1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bookmark_count(self):
        for i in range(3):
            self.client.force_authenticate(user=self.users[i])
            data = {
                'restaurant': self.test_restaurant.id
            }
            response = self.client.post('/api/bookmark', data=data)

        self.assertEqual(BookMark.objects.filter(restaurant=self.test_restaurant).count(), 3)