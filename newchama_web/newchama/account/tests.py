from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
# Create your tests here.


class MemberTestCase(TestCase):
        def test_password(self):
            str_password = make_password("111111", "Vkv4oyxHy4VB")
            self.assertEquals(str_password, "pbkdf2_sha256$12000$Vkv4oyxHy4VB$sx4nGA+Mc8tbz4JWz")

