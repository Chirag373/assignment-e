from django.http import HttpResponse
from rest_framework.views import APIView
from .services import StudentReportService
from .format import error_response

class StudentReportAPIView(APIView):
    def get(self, request, id):
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
            
        cookies = request.COOKIES
            
        pdf_bytes, error, status_code = StudentReportService.generate_report(id, headers, cookies)
        
        if error:
            return error_response(
                error_message=error.get("error", "Failed to generate report"),
                details=error.get("details"),
                status_code=status_code
            )
            
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_{id}_report.pdf"'
        return response


