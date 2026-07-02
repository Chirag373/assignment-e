from django.urls import path
from .views import StudentReportAPIView

urlpatterns = [
    path('students/<int:id>/report', StudentReportAPIView.as_view(), name='student-report'),
]
