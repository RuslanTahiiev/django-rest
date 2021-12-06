import json
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from homeapp.models import SiteUpdateNews, UserUpdateNewsRelation
from homeapp.serializers import SiteUpdateNewsSerializer


class HomeApiTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username='test_username')
        self.fake_user = User.objects.create(username='fake_username')
        self.staff_user = User.objects.create(username='staff_username', is_staff=True)

        self.update_news_1 = SiteUpdateNews.objects.create(
            title='Run DB',
            intro='some intro',
            text='Это тест.',
            owner=self.user,
        )
        self.update_news_2 = SiteUpdateNews.objects.create(
            title='some title',
            intro='Run DB',
            text=''
        )
        self.update_news_3 = SiteUpdateNews.objects.create(
            title='title',
            intro='intro',
            text='text'
        )
        self.update_news_4 = SiteUpdateNews.objects.create(
            title='1',
            intro='2',
            text='3'
        )

    # GET METHOD #
    def test_get_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_siteupdatenews(self):

        url = reverse('siteupdatenews-list')
        response = self.client.get(url)
        serializer_data = SiteUpdateNewsSerializer([self.update_news_1, self.update_news_2,
                                                    self.update_news_3, self.update_news_4], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_siteupdatenews_search(self):

        url = reverse('siteupdatenews-list')
        response = self.client.get(url, data={'search': 'title'})
        serializer_data = SiteUpdateNewsSerializer([self.update_news_2, self.update_news_3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_siteupdatenews_filtering(self):

        url = reverse('siteupdatenews-list')
        response = self.client.get(url, data={'title': '1'})
        serializer_data = SiteUpdateNewsSerializer([self.update_news_4], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_siteupdatenews_ordering(self):

        url = reverse('siteupdatenews-list')
        response = self.client.get(url, data={'ordering': '-date'})
        queryset = SiteUpdateNews.objects.all().order_by('-date')
        serializer_data = SiteUpdateNewsSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    # POST METHOD #
    def test_create_siteupdatenews(self):

        self.assertEqual(4, SiteUpdateNews.objects.all().count())

        url = reverse('siteupdatenews-list')

        data = {
                'title': 'TestTitle',
                'intro': 'TestIntro',
                'text': 'TestText'
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)

        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, SiteUpdateNews.objects.all().count())
        self.assertEqual(self.user, SiteUpdateNews.objects.last().owner)

    # UPDATE METHOD #
    def test_update_siteupdatenews(self):

        url = reverse('siteupdatenews-detail', args=(self.update_news_1.id, ))

        data = {
                'title': self.update_news_1.title,
                'intro': 'TestIntroPut',
                'text': self.update_news_1.text
        }

        json_data = json.dumps(data)

        self.client.force_login(self.user)

        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.update_news_1.refresh_from_db()
        self.assertEqual('TestIntroPut', self.update_news_1.intro)

    def test_not_owner_update_siteupdatenews(self):

        url = reverse('siteupdatenews-detail', args=(self.update_news_1.id, ))

        data = {
                'title': self.update_news_1.title,
                'intro': 'TestIntroPut',
                'text': self.update_news_1.text
        }

        json_data = json.dumps(data)

        self.client.force_login(self.fake_user)

        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')}, response.data)
        self.update_news_1.refresh_from_db()
        self.assertEqual('some intro', self.update_news_1.intro)

    def test_not_owner_but_staff_update_siteupdatenews(self):
        url = reverse('siteupdatenews-detail', args=(self.update_news_1.id,))

        data = {
            'title': self.update_news_1.title,
            'intro': 'TestIntroPut',
            'text': self.update_news_1.text
        }

        json_data = json.dumps(data)

        self.client.force_login(self.staff_user)

        response = self.client.put(url, data=json_data,
                                   content_type='application/json')


        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.update_news_1.refresh_from_db()
        self.assertEqual('TestIntroPut', self.update_news_1.intro)

    # DELETE METHOD #
    def test_delete_siteupdatenews(self):

        test_id = self.update_news_1.id
        url = reverse('siteupdatenews-detail', args=(test_id, ))

        self.client.force_login(self.user)

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Http404):
            get_object_or_404(SiteUpdateNews, id=test_id)

    def test_not_owner_delete_siteupdatenews(self):

        test_id = self.update_news_1.id
        url = reverse('siteupdatenews-detail', args=(test_id, ))

        self.client.force_login(self.fake_user)

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')}, response.data)

    def test_not_owner_but_staff_delete_siteupdatenews(self):

        test_id = self.update_news_1.id
        url = reverse('siteupdatenews-detail', args=(test_id, ))

        self.client.force_login(self.staff_user)

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Http404):
            get_object_or_404(SiteUpdateNews, id=test_id)


class UserUpdateNewsRelationTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username='test_username')
        self.fake_user = User.objects.create(username='fake_username')
        self.staff_user = User.objects.create(username='staff_username', is_staff=True)

        self.update_news_1 = SiteUpdateNews.objects.create(
            title='Run DB',
            intro='some intro',
            text='Это тест.',
            owner=self.user,
        )

    # PATCH METHOD #
    def test_patch_user_news_rel(self):

        url = reverse('userupdatenewsrelation-detail', args=(self.update_news_1.id, ))

        data = {
            'like': True,
        }

        self.client.force_login(self.user)

        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        relation_news_user = UserUpdateNewsRelation.objects.get(update_news=self.update_news_1.id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation_news_user.refresh_from_db()
        self.assertTrue(relation_news_user.like)

