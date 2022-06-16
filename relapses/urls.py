from django.urls import path

from relapses.api.views import RelapseAPIView, RelapseListAPIView, RelapseReportAPIView

urlpatterns = [
    path('relapse/<int:id>/', RelapseAPIView.as_view()),
    path('relapses/', RelapseListAPIView.as_view()),
    path('relapse/report/', RelapseReportAPIView.as_view())
]
