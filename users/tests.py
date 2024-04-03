from django.contrib.auth.models import User

from apps.tests import BaseTestCase


class TestLogout(BaseTestCase):
    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class TestSettings(BaseTestCase):
    def test_settings(self):
        self.login()
        response = self.client.get('/users/settings/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/settings/profile')

    def test_settings_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/settings/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/settings/')


class TestProfileSettings(BaseTestCase):
    def test_profile_settings(self):
        self.login()
        response = self.client.get('/users/settings/profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_settings_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/settings/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/settings/profile')


class TestStaffManagement(BaseTestCase):
    def test_staff_management(self):
        self.login()
        self.set_as_superuser()
        response = self.client.get('/users/staff_management/')
        self.assertEqual(response.status_code, 200)

    def test_staff_management_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/staff_management/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/')

    def test_staff_management_not_superuser(self):
        self.login()
        response = self.client.get('/users/staff_management/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/')


class TestStaffManagementAdd(BaseTestCase):
    def test_staff_management_add_get(self):
        self.login()
        self.set_as_superuser()
        response = self.client.get('/users/staff_management/manage/add')
        self.assertEqual(response.status_code, 200)

    def test_staff_management_add_get_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/staff_management/manage/add')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/add')

    def test_staff_managementv_add_not_superuser(self):
        self.login()
        response = self.client.get('/users/staff_management/manage/add')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/add')

    def test_staff_management_add_post(self):
        self.login()
        self.set_as_superuser()
        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/staff_management/')
        self.assertTrue(self.client.login(username='test', password='testpassword'))
        response = self.client.get('/users/staff_management/')
        self.assertEqual(response.status_code, 200)

    def test_staff_management_add_post_not_logged_in(self):
        self.logout()
        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/add')

    def test_staff_management_add_post_not_superuser(self):
        self.login()
        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/add')

    def test_staff_management_add_post_invalid(self):
        self.login()
        self.set_as_superuser()
        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.', count=1)

        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': False
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': False
        })
        self.assertEqual(response.status_code, 200)


class TestStaffManagementEdit(BaseTestCase):
    def create_dummy_user(self):
        self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': False
        })

    def test_staff_management_add_get(self):
        self.login()
        self.set_as_superuser()
        self.create_dummy_user()
        response = self.client.get('/users/staff_management/manage/edit/1')
        self.assertEqual(response.status_code, 200)

    def test_staff_management_add_get_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/staff_management/manage/edit/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/edit/1')

    def test_staff_management_add_not_superuser(self):
        self.login()
        response = self.client.get('/users/staff_management/manage/edit/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/edit/1')

    def test_staff_management_add_post(self):
        self.login()
        self.set_as_superuser()
        self.create_dummy_user()
        response = self.client.post('/users/staff_management/manage/edit/2', {
            'username': 'test2',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(id=2).is_superuser, True)
        self.assertEqual(User.objects.get(id=2).username, 'test2')

    def test_staff_management_add_post_invalid(self):
        self.login()
        self.set_as_superuser()
        self.create_dummy_user()
        response = self.client.post('/users/staff_management/manage/edit/2', {
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', count=1)

    def test_staff_management_add_post_not_logged_in(self):
        self.logout()
        response = self.client.post('/users/staff_management/manage/edit/1', {
            'username': 'test2',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/edit/1')

    def test_staff_management_add_post_not_superuser(self):
        self.login()
        self.create_dummy_user()
        response = self.client.post('/users/staff_management/manage/edit/2', {
            'username': 'test2',
            'is_superuser': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/edit/2')


class TestStaffManagementDisable(BaseTestCase):
    def create_dummy_user(self):
        self.client.post('/users/staff_management/manage/add', {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_superuser': False
        })

    def test_staff_management_disable(self):
        self.login()
        self.set_as_superuser()
        self.create_dummy_user()
        response = self.client.get('/users/staff_management/manage/disable/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/staff_management/')
        self.assertEqual(User.objects.get(id=1).is_active, True)
        self.assertEqual(User.objects.get(id=2).is_active, False)
        response = self.client.get('/users/staff_management/manage/disable/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/staff_management/')
        self.assertEqual(User.objects.get(id=1).is_active, True)
        self.assertEqual(User.objects.get(id=2).is_active, True)

    def test_staff_management_disable_yourself(self):
        self.login()
        self.set_as_superuser()
        response = self.client.get('/users/staff_management/manage/disable/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/staff_management/')
        self.assertEqual(User.objects.get(id=1).is_active, True)

    def test_staff_management_disable_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/staff_management/manage/disable/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/disable/1')

    def test_staff_management_disable_not_superuser(self):
        self.login()
        self.create_dummy_user()
        response = self.client.get('/users/staff_management/manage/disable/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/staff_management/manage/disable/1')


class TestUserManagement(BaseTestCase):
    def test_user_management(self):
        self.login()
        self.set_as_superuser()
        response = self.client.get('/users/users_management/')
        self.assertEqual(response.status_code, 200)

    def test_user_management_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/users_management/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/users_management/')


class TestUserDetail(BaseTestCase):
    def create_dummy_user(self):
        User.objects.create_user(
            username='test',
            password='testpassword'
        )

    def test_user_detail(self):
        self.login()
        self.set_as_superuser()
        self.create_dummy_user()
        response = self.client.get('/users/users_management/manage/2')
        self.assertEqual(response.status_code, 200)

    def test_user_detail_not_logged_in(self):
        self.logout()
        response = self.client.get('/users/users_management/manage/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/users_management/manage/1')

    def test_user_detail_not_superuser(self):
        self.login()
        self.create_dummy_user()
        response = self.client.get('/users/users_management/manage/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/users/users_management/manage/2')