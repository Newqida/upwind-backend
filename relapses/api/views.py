from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated

from relapses.api.serializers import RelapseSerializer, RelapseCreateSerializer, RelapseReportSerializer
from relapses.models import Relapse


class RelapseListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        habit = self.request.data.get('habit', None)
        if habit == None:
            return Relapse.objects.filter(user=self.request.user)
        else:
            return Relapse.objects.filter(user=self.request.user, habit=habit)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RelapseCreateSerializer
        else:
            return RelapseSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.data['user'] = request.user.pk
            return super().create(request, *args, **kwargs)
        else:
            raise NotAuthenticated()


class RelapseAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_calss = RelapseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Relapse.objects.filter(user=self.request.user)


class RelapseReportAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    serializer_class = RelapseReportSerializer

    def get(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.generate_report(request.user)
        return Response(report)
