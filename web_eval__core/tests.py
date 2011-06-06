from django.test import TestCase
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


class AuthTest(TestCase):
    def authenticate(self):
        self.failUnlessEqual(1 + 1, 2)


