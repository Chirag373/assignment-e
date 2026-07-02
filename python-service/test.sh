#!/bin/bash

echo "1. Logging in to get the JWT cookies and CSRF token..."
curl -c cookies.txt -s -X POST http://localhost:5007/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@school-admin.com","password":"3OU4zn3q6Zh9"}' > /dev/null

echo "2. Extracting the CSRF token from the cookie file..."
CSRF=$(awk '/csrfToken/ {print $7}' cookies.txt)
echo "Found CSRF Token: $CSRF"

echo "3. Fetching the PDF report using the cookies and the CSRF token..."
curl -s -b cookies.txt -H "x-csrf-token: $CSRF" \
  -o test_report_5.pdf \
  -w "HTTP Status: %{http_code}\n" \
  http://localhost:8000/api/v1/students/5/report

echo "Done! Check if test_report_5.pdf was created."
