from django.contrib.auth.models import User
from django.test import TestCase
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation
from homeapp.serializers import SiteUpdateNewsSerializer


class SiteUpdateNewsSerializerTestCase(TestCase):

    def test_siteupdatenewsserializer(self):

        user1 = User.objects.create(username='username1')
        user2 = User.objects.create(username='username2')
        user3 = User.objects.create(username='username3')

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

        UserUpdateNewsRelation.objects.create(user=user1, update_news=update_news_1, like=True)
        UserUpdateNewsRelation.objects.create(user=user2, update_news=update_news_1, like=True)
        UserUpdateNewsRelation.objects.create(user=user3, update_news=update_news_1, like=True)

        UserUpdateNewsRelation.objects.create(user=user1, update_news=update_news_2, like=True)
        UserUpdateNewsRelation.objects.create(user=user2, update_news=update_news_2, like=True)
        UserUpdateNewsRelation.objects.create(user=user3, update_news=update_news_2, like=False)

        serializer_data = SiteUpdateNewsSerializer([update_news_1, update_news_2], many=True).data

        expected_data = [
            {
                'id': update_news_1.id,
                'title': 'Запустили БД',
                'intro': 'Теперь работает БД',
                'text': 'Это тест.',
                'date': update_news_1.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 3,
            },
            {
                'id': update_news_2.id,
                'title': 'Запустили БД #2',
                'intro': 'Теперь работает БД #2',
                'text': '',
                'date': update_news_2.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 2,
            }
        ]
        self.assertEqual(expected_data, serializer_data)
