from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Restaurant
from review.models import Review


class RestaurantTestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(3):
            Restaurant.objects.create(
                rest_name=f'abc{i}마켓',
                rest_star=2.9,
                rest_address='seoul',
                rest_phone_number='010299000',
                rest_food='한식',
                rest_sale='만원대',
                rest_time=f'오전10시~오후 1{i}시',
                rest_break_time=f'{i}시~6시',
                rest_count=i
            )

        self.test_restaurants = Restaurant.objects.all()
        self.user = baker.make('auth.User', _quantity=1)

        self.review=Review.objects.create(review_text="아주 맛있꾸미", taste_value="GOOD", owner_rest=self.test_restaurants[0],
                              owner_user=self.user[0])

    def test_should_list_restaurant(self):
        """
        Request : GET - /api/restaurant/
        """
        response = self.client.get('/api/restaurant')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for test_rest, response_rest in zip(self.test_restaurants, response.data['results']):
            self.assertEqual(test_rest.id, response_rest['id'])
            self.assertEqual(test_rest.rest_name, response_rest['rest_name'])
            self.assertEqual(test_rest.rest_star, response_rest['rest_star'])
            self.assertEqual(test_rest.rest_address, response_rest['rest_address'])
            self.assertEqual(test_rest.rest_phone_number, response_rest['rest_phone_number'])
            self.assertEqual(test_rest.rest_food, response_rest['rest_food'])
            self.assertEqual(test_rest.rest_sale, response_rest['rest_sale'])
            self.assertEqual(test_rest.rest_time, response_rest['rest_time'])
            self.assertEqual(test_rest.rest_break_time, response_rest['rest_break_time'])

    def test_should_detail_restaurant(self):
        """
        Request : GET - /api/restaurant/{restaurant_id}
        """
        test_restaurant = self.test_restaurants[0]
        response = self.client.get(f'/api/restaurant/{test_restaurant.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(test_restaurant.id, response.data['id'])
        self.assertEqual(test_restaurant.rest_name, response.data['rest_name'])
        self.assertEqual(test_restaurant.rest_star, response.data['rest_star'])
        self.assertEqual(test_restaurant.rest_address, response.data['rest_address'])
        self.assertEqual(test_restaurant.rest_phone_number, response.data['rest_phone_number'])
        self.assertEqual(test_restaurant.rest_food, response.data['rest_food'])
        self.assertEqual(test_restaurant.rest_sale, response.data['rest_sale'])
        self.assertEqual(test_restaurant.rest_time, response.data['rest_time'])
        self.assertEqual(test_restaurant.rest_sale, response.data['rest_sale'])
        self.assertEqual(test_restaurant.rest_break_time, response.data['rest_break_time'])
        self.assertTrue(response.data['owner_rest'][0]['id'])
