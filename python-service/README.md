# Python Service - Student Report Generation

This service handles the generation of PDF reports for students using WeasyPrint and Django. It communicates directly with the Node.js backend to fetch student data and returns a formatted PDF.

## 🚀 Setup Instructions

1. **Navigate to the python-service directory**
   ```bash
   cd python-service
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have system-level dependencies for WeasyPrint installed if you encounter issues during PDF generation, such as `pango`, `cairo`, and `gdk-pixbuf`).*

4. **Run the server**
   ```bash
   python manage.py runserver 8000
   ```

   The service will start on `http://localhost:8000`.

---

## 🧪 How to Test

Because the Node.js backend requires strict security measures (both a JWT **accessToken** cookie and a **CSRF token** header), you cannot easily test this endpoint via a simple browser URL visit. The Python service correctly forwards these security tokens to the Node backend.

### Option 1: Automated Test Script (Recommended)
You can use the provided bash script (`test.sh`) to automatically log in, extract the required tokens, and download a sample PDF report.

1. Ensure the Node.js backend (`:5007`) and this Python service (`:8000`) are running.
2. In the `python-service` directory, run the test script:
   ```bash
   chmod +x test.sh
   ./test.sh
   ```
   This script will authenticate as the admin, extract the CSRF token, and make a request to `/api/v1/students/5/report`. It will save the resulting PDF as `test_report_5.pdf` in your directory.

### Option 2: Manual Testing via cURL
If you prefer to run the commands yourself, here is the exact two-step process to bypass the security middleware correctly:

**1. Login and save session cookies:**
```bash
curl -c cookies.txt -s -X POST http://localhost:5007/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@school-admin.com","password":"3OU4zn3q6Zh9"}'
```

**2. Extract the CSRF token and fetch the report:**
```bash
# Extract the CSRF token from the cookie file
CSRF=$(awk '/csrfToken/ {print $7}' cookies.txt)

# Use the cookies (-b) and the CSRF header (-H) to hit the python service
curl -s -b cookies.txt -H "x-csrf-token: $CSRF" \
  -o student_report.pdf \
  http://localhost:8000/api/v1/students/5/report
```
