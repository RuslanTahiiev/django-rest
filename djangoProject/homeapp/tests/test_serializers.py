from django.test import TestCase
from homeapp.models import SiteUpdateNews
from homeapp.serializers import SiteUpdateNewsSerializer


class SiteUpdateNewsSerializerTestCase(TestCase):

    def test_siteupdatenewsserializer(self):

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

        serializer_data = SiteUpdateNewsSerializer([update_news_1, update_news_2], many=True).data

        expected_data = [
            {
                'id': update_news_1.id,
                'title': 'Запустили БД',
                'intro': 'Теперь работает БД',
                'text': 'Это тест.',
                'date': update_news_1.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            },
            {
                'id': update_news_2.id,
                'title': 'Запустили БД #2',
                'intro': 'Теперь работает БД #2',
                'text': '',
                'date': update_news_2.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
        ]
        self.assertEqual(expected_data, serializer_data)
