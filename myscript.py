from datetime import datetime

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Daily Report</title>
</head>
<body>
    <b>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</b>
    <p>This is an automated HTML report.</p>
</body>
</html>
"""

with open("report.html", "w") as file:
    file.write(html_content)

print("HTML file generated successfully.")
