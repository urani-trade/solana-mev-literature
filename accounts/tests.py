from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import login_view, logout_view, register_view
from .forms import UserLoginForm, UserRegisterForm

User = get_user_model()


class TestUrls(SimpleTestCase):

    def test_login_view_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_view_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func,  logout_view)

    def test_register_view_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_view)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.fixtures = ['test_db.json']
        self.user = User.objects.create_user('newuser',
                                        'newuser@example.com',
                                        'testing321')
        self.data =  {
            'username': 'newuser',
            'password': 'testing321'
        }

    def test_login_unauthenticated_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_authenticated_GET(self):
        self.client.login(username='newuser', password='testing321')
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], reverse('index'))

    def test_login_POST(self):
        response = self.client.post(reverse('login'), data=self.data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register_unauthenticated_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_authenticated_GET(self):
        self.client.login(username='newuser', password='testing321')
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], reverse('index'))

    def test_register_POST(self):
        client = Client()
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testing321',
            'password_confirm': 'testing321'
        }
        response = client.post(reverse('register'), data=data, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_logout_unauthenticated_GET(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], '/accounts/login/?next=/accounts/logout/')

    def test_logout_authenticated_GET(self):
        self.client.login(username='newuser', password='testing321')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')


class TestForms(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('newuser',
                                        'newuser@example.com',
                                        'testing321')
        self.form_data = {
            'username': 'newuser',
            'password': 'testing321'
        }
        self.bad_credentials = {
            'username': 'asdfasdf',
            'password': 'testing321'
        }

    def test_user_login_form_is_valid(self):
        form = UserLoginForm(data=self.form_data)
        bad_credentials_form = UserLoginForm(data=self.bad_credentials)
        self.assertTrue(form.is_valid())
        self.assertFalse(bad_credentials_form.is_valid())

    def test_user_register_form_is_valid(self):
        password_too_short_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testing',
            'password_confirm': 'testing'
        }

        passwords_do_not_match_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testingasdfasdfasdf',
            'password_confirm': 'testing321'
        }

        no_username_data = {
            'email': 'newuser@example.com',
            'password': 'testing321',
            'password_confirm': 'testing321'
        }

        username_taken_data = {
            'username': 'newuser2',
            'email': 'email@email.com',
            'password': 'testing321',
            'password_confirm': 'testing321'
        }

        email_taken_data = {
            'username': 'newuser',
            'email': 'newuser2@example.com',
            'password': 'testing321',
            'password_confirm': 'testing321'
        }

        no_username_form = UserRegisterForm(data=no_username_data)
        password_too_short_form = UserRegisterForm(data=password_too_short_data)
        passwords_do_not_match_form = UserRegisterForm(data=passwords_do_not_match_data)
        username_taken_form = UserRegisterForm(data=username_taken_data)
        email_taken_form = UserRegisterForm(data=email_taken_data)

        self.assertFalse(no_username_form.is_valid())
        self.assertFalse(password_too_short_form.is_valid())
        self.assertFalse(passwords_do_not_match_form.is_valid())
        self.assertFalse(username_taken_form.is_valid())
        self.assertFalse(email_taken_form.is_valid())

    def test_user_login_form_non_field_errors(self):
        suspended_user = User.objects.create_user('newuser2', 'newuser2@example.com', 'testing321')
        suspended_user.is_active = False
        suspended_user.save()
        suspended_user_data = {
            'username': 'newuser2',
            'password': 'testing321'
        }
        response = self.client.post(reverse('login'), data=suspended_user_data, follow=True)
        self.assertFormError(response, 'form', field=None, errors='Username password combination does not exist')
