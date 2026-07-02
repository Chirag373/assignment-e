import os
import requests
from django.conf import settings
from weasyprint import HTML
from django.template import Context, Template

class StudentReportService:
    NODE_API_BASE_URL = "http://localhost:5007/api/v1"

    @classmethod
    def generate_report(cls, student_id, headers, cookies=None):
        url = f"{cls.NODE_API_BASE_URL}/students/{student_id}"
        resp = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        if resp.status_code != 200:
            return None, {"error": "Failed to fetch student data", "details": resp.text}, resp.status_code
            
        student_data = resp.json().get('data', resp.json())
        
        # Clean data for the template (flat key-value pairs, formatted keys)
        clean_data = {
            str(k).replace('_', ' ').title(): v 
            for k, v in student_data.items() 
            if not isinstance(v, (dict, list))
        }
        
        # Scalable HTML-based layout
        template = Template("""
        <html>
        <head>
            <style>
                body { font-family: Helvetica, sans-serif; padding: 30px; color: #333; }
                h1 { text-align: center; border-bottom: 2px solid #2c3e50; padding-bottom: 15px; color: #2c3e50; }
                table { width: 100%; border-collapse: collapse; margin-top: 25px; }
                th, td { border: 1px solid #ecf0f1; padding: 12px 15px; text-align: left; }
                th { background-color: #f8f9fa; width: 35%; color: #2c3e50; }
                tr:nth-child(even) { background-color: #fbfbfc; }
            </style>
        </head>
        <body>
            <h1>Student Report</h1>
            <table>
                {% for key, value in data.items %}
                    <tr>
                        <th>{{ key }}</th>
                        <td>{{ value }}</td>
                    </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """)
        
        html_content = template.render(Context({'data': clean_data}))
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        # Save the generated PDF locally
        reports_dir = os.path.join(settings.BASE_DIR, 'student_reports')
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, f'student_{student_id}_report.pdf')
        
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)
            

        
        return pdf_bytes, None, 200
