from djoser import utils
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class UserByToken(APIView):

    def post(self, request, format=None):
        data = {
            'id': str(request.user.id),
            'username': str(request.user.username)
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance == request.user:
            if not instance.is_superuser:
                utils.logout_user(self.request)
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)




