import csv
import webbrowser
import os
from datetime import datetime as dt
import sys

#Check if arguments were passed to the script
if len(sys.argv) > 1:
    # Path to the CSV file
    csv_path = sys.argv[1]
    # Path to the generated HTML file
    html_path = sys.argv[2]
    # Path to the HTML template
    template_path = sys.argv[3]
    # Path to the HTML template
    open_after = sys.argv[4]
else:
    # Path to the CSV file
    csv_path = 'results.csv'
    # Path to the generated HTML file
    html_path = 'results.html'
    # Path to the HTML template
    template_path = 'ReportTemplate.html'
    # Path to the HTML template
    open_after = 'True'

print("CSV Path: ", csv_path)
print("HTML Path: ", html_path)
print("Template Path: ", template_path)

# Read the CSV file
with open(csv_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Extract header information from the first row
header_info = [(rows[0][i].strip(), rows[0][i + 1].strip()) for i in range(0, len(rows[0]), 2)]

# Read the HTML template
with open(template_path, 'r') as templatefile:
    html_template = templatefile.read()

# Generate the header section dynamically
header_section = ''
for key, value in header_info:
    header_section += '<div>{}: {}</div>'.format(key, value)

# Replace the header placeholder with the generated header section
html_template = html_template.replace('<!--HEADER_SECTION-->', header_section)

# Generate table headers
table_headers = ''.join(['<th>{}</th>'.format(header) for header in rows[1]])  # Assuming headers are in the second row
html_template = html_template.replace('<!--TABLE_HEADERS-->', table_headers)

# Generate table rows and count pass/fail
table_rows = ''
test_passed = 0
test_failed = 0
total_steps = 0

# Extract start and end times
start_time_str = "{} {}".format(rows[2][0], rows[2][1])
end_time_str = "{} {}".format(rows[-1][0], rows[-1][1])

# Parse the start and end times
start_time = dt.strptime(start_time_str, '%d/%m/%Y %H:%M:%S')
end_time = dt.strptime(end_time_str, '%d/%m/%Y %H:%M:%S')

# Calculate test duration
test_duration = end_time - start_time

# Break down the test duration into days, hours, and minutes
days = test_duration.days
hours, remainder = divmod(test_duration.seconds, 3600)
minutes, _ = divmod(remainder, 60)

# Format the test duration string
test_duration_str = "{} day{}, {} hour{}, {} minute{}".format(
    days, 's' if days != 1 else '',
    hours, 's' if hours != 1 else '',
    minutes, 's' if minutes != 1 else ''
)

# Generate table rows
for row in rows[2:]:
    total_steps += 1
    status = 'PASS' if 'PASS' in row else 'FAIL'
    if status == 'PASS':
        test_passed += 1
        row_class = ''
    else:
        test_failed += 1
        row_class = ' class="failed-row"'
    table_row = '<tr{} data-status="{}">'.format(row_class, status)
    for i in range(len(row)):
        if i == len(row) - 1 and len(row) < len(rows[1]):  # If we're at the last entry and the number of cells in the row is less than the number of headers
            table_row += '<td colspan="{}"><b>Message: </b>{}</td>'.format(len(rows[1]) - i, row[i])  # Add the colspan attribute to the last cell
        else:
            table_row += '<td>{}</td>'.format(row[i])  # Add <td> tags to each cell
    table_row += '</tr>'
    table_rows += table_row

# Replace placeholders in the HTML template
html_template = html_template.replace('<!--TABLE_ROWS-->', table_rows)
html_template = html_template.replace('<!--TEST_PASSED-->', str(test_passed))
html_template = html_template.replace('<!--TEST_FAILED-->', str(test_failed))
html_template = html_template.replace('<!--TOTAL_STEPS-->', str(total_steps))
html_template = html_template.replace('<!--TEST_DURATION-->', test_duration_str)

# Determine test status
if test_failed > 0:
    test_status_class = 'test-failed'
    test_status_message = 'Failed'
else:
    test_status_class = 'test-passed'
    test_status_message = 'Passed'

html_template = html_template.replace('<!--TEST_STATUS_CLASS-->', test_status_class)
html_template = html_template.replace('<!--TEST_STATUS_MESSAGE-->', test_status_message)

# Save the generated HTML report
with open(html_path, 'w') as outputfile:
    outputfile.write(html_template)

if(open_after == 'True'):
    # Optionally open the generated HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_path))