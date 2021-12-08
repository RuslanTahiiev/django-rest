from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, F
from django.test import TestCase
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation
from homeapp.serializers import SiteUpdateNewsSerializer


class SiteUpdateNewsSerializerTestCase(TestCase):

    def test_siteupdatenewsserializer(self):

        user1 = User.objects.create(username='username1', first_name='F1', last_name='L1')
        user2 = User.objects.create(username='username2', first_name='F2', last_name='L2')
        user3 = User.objects.create(username='username3', first_name='F3', last_name='L3')

        update_news_1 = SiteUpdateNews.objects.create(
            title='Запустили БД',
            intro='Теперь работает БД',
            text='Это тест.',
            owner=user1,
        )
        update_news_2 = SiteUpdateNews.objects.create(
            title='Запустили БД #2',
            intro='Теперь работает БД #2',
            text='',
            owner=user2,
        )

        UserUpdateNewsRelation.objects.create(user=user1, update_news=update_news_1, like=True, rate=5)
        UserUpdateNewsRelation.objects.create(user=user2, update_news=update_news_1, like=True, rate=4)
        UserUpdateNewsRelation.objects.create(user=user3, update_news=update_news_1, like=True, rate=2)

        UserUpdateNewsRelation.objects.create(user=user1, update_news=update_news_2, like=True, rate=3)
        UserUpdateNewsRelation.objects.create(user=user2, update_news=update_news_2, like=True, rate=4)
        UserUpdateNewsRelation.objects.create(user=user3, update_news=update_news_2, like=False)

        news = SiteUpdateNews.objects.all().annotate(
            annotated_likes=Count(Case(When(userupdatenewsrelation__like=True, then=1))),
            rating=Avg('userupdatenewsrelation__rate'),
            owner_name=F('owner__username'),
        ).order_by('id')

        serializer_data = SiteUpdateNewsSerializer(news, many=True).data

        expected_data = [
            {
                'id': update_news_1.id,
                'title': 'Запустили БД',
                'intro': 'Теперь работает БД',
                'text': 'Это тест.',
                'date': update_news_1.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'annotated_likes': 3,
                'rating': '3.67',
                'owner_name': 'username1',
                'watchers': [
                    {
                        'first_name': 'F1',
                        'last_name': 'L1',
                    },
                    {
                        'first_name': 'F2',
                        'last_name': 'L2',
                    },
                    {
                        'first_name': 'F3',
                        'last_name': 'L3',
                    },
                ],
            },
            {
                'id': update_news_2.id,
                'title': 'Запустили БД #2',
                'intro': 'Теперь работает БД #2',
                'text': '',
                'date': update_news_2.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': 'username2',
                'watchers': [
                    {
                        'first_name': 'F1',
                        'last_name': 'L1',
                    },
                    {
                        'first_name': 'F2',
                        'last_name': 'L2',
                    },
                    {
                        'first_name': 'F3',
                        'last_name': 'L3',
                    },
                ],
            }
        ]
        self.assertEqual(expected_data, serializer_data)
