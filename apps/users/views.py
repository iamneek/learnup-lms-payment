from rest_framework.views import APIView, Response
# Create your views here.


class UserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"message": "Hello, World!"})
