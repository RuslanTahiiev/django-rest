from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from homeapp.models import SiteUpdateNews
from homeapp.serializers import SiteUpdateNewsSerializer


class HomeApiTestCase(APITestCase):

    def test_get_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_siteupdatenews(self):
        update_news_1 = SiteUpdateNews.objects.create(
            title='Запустили БД',
            intro='Теперь работает БД',
            text='Это тест.'
        )
        update_news_2 = SiteUpdateNews.objects.create(
            title='Запустили БД #2',
            intro='Теперь работает БД #2',
            text=''
        )

        url = reverse('siteupdatenews-list')
        response = self.client.get(url)
        serializer_data = SiteUpdateNewsSerializer([update_news_1, update_news_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
