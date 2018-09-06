# from django.contrib.auth.models import AbstractUser, BaseUserManager
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **kwars):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password):
#         user = self.create_user(
#             email, password=password
#         )
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractUser):
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email
#
#
# User._meta.get_field('email')._unique = True
# User._meta.get_field('username')._unique = False
