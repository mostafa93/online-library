from django.test import TestCase
from OnlineBookLibrary.models import Library
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Authentication(TestCase):

    def test_sign_up_correct_info(self):
        response = self.client.post(
            '/onlinebooklibrary/user/new/', {'username': 'mostafa',
                                             'email': 'mostafa@gmail.com',
                                             'password1': 'thekey',
                                             'password2': 'thekey'})
        self.assertEquals(response.status_code, 302)

    def test_sign_up_missmatching_password(self):
        response = self.client.post(
            reverse('user-new'), {'username': 'ahmad',
                                  'email': 'ahmad@gmail.com',
                                  'password1': 'thekey',
                                  'password2': 'the'})
        # self.assertRedirects(response.url, '/onlinebooklibrary/user/new/',
        # status_code=200, target_status_code=200, msg_prefix='')
        self.assertEquals(response.status_code, 200)
        bool = 0
        try:
            User.objects.get(username='ahmad')
            bool = 1
        except:
            pass
        self.assertEquals(bool, 0)

    def test_sign_up_no_email(self):
        response = self.client.post(
            reverse('user-new'), {'username': 'ahmad',
                                  'email': '',
                                  'password1': 'thekey',
                                  'password2': 'thekey'})
        self.assertEquals(response.status_code, 200)
        bool = 0
        try:
            User.objects.get(username='ahmad')
            bool = 1
        except:
            pass
        self.assertEquals(bool, 0)


class Libraries(TestCase):

    def test_create_library_logged_in(self):
        user = User.objects.create_user(username='mostafa', password='thekey')
        self.client.login(username='mostafa', password='thekey')
        response = self.client.post(
            reverse('library-new'), {'library_name': 'kotob khan',
                                     'library_owner': user.id})
        library = Library.objects.get(library_owner_id=user.id)
        self.assertEquals(library.library_name, 'kotob khan')
        self.assertEquals(response.status_code, 302)

    def test_create_library_logged_out(self):
        user = User.objects.create_user(username='mostafa', password='thekey')
        self.client.post(
            reverse('library-new'), {'library_name': 'kotob khan',
                                     'library_owner': user.id})
        bool = 0
        try:
            Library.objects.get(library_owner_id=user.id)
            bool = 1
        except:
            pass
        self.assertEquals(bool, 0)

    def test_library_list_view(self):
        user1 = User.objects.create_user(username='mostafa', password='thekey')
        user2 = User.objects.create_user(
            username='mostafa2', password='thekey')
        Library.objects.create(
            library_name='kotob khan', library_owner_id=user1.id)
        Library.objects.create(
            library_name='alef book store', library_owner_id=user2.id)
        response = self.client.get(reverse('library-list'))
        self.assertEquals(
            response.context['library_list'][0].library_name, 'kotob khan')
        self.assertEquals(
            response.context['library_list'][1].library_name,
            'alef book store')

