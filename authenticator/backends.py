# # myapp/backends.py
# from django.contrib.auth.backends import BaseBackend
# from .models import StudentUser
#
#
# class MyAuthBackend(BaseBackend):
#
#     def authenticate(self, request, username=None, password=None, ):
#         try:
#             user = StudentUser.objects.get(username=username)
#             if user.password == password:
#                 return user
#         except StudentUser.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return StudentUser.objects.get(pk=user_id)
#         except StudentUser.DoesNotExist:
#             return None
