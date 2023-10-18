from pyexcel_ods3 import get_data
from behave import given, when, then, step
from datetime import date
import webbrowser
from pyhtml2pdf import converter


@step('Docs API: Verify if "{query}" {condition} exist in ODS file')
def is_message_in_ods_file(context, query, condition):
    assert condition in ['should', 'should not'], f"The condition must be 'should' or 'should not'"

    if query == 'company':
        query = context.company

    file = context.path_to_ods

    data = get_data(file)
    companies = []
    for i in range(1, len(data['Sheet1']) - 1):
        company = data['Sheet1'][i]
        if len(company) > 0:
            companies.append(company[0].lower())

    if condition == 'should' and query.lower() not in companies:
        raise ValueError(f"{query} is not found in {file}")
    elif condition == 'should not' and query.lower() in companies:
        raise ValueError(f"{query} is found in {file}")
    elif condition == 'should' and query.lower() in companies:
        print(f"{query} is found in {file}")
    elif condition == 'should not' and query.lower() not in companies:
        print(f"{query} is not found in {file}")


@step('Docs API: Remove the positions that have been rejected from the list of found on "{source}"')
def update_found(context, source):
    assert source.lower() in ['indeed'], f"The resource should be 'Indeed', 'LinkedIn', 'ZipRecruiter', 'DICE'"

    list_before = []
    list_updated = []
    if source.lower() == 'indeed':
        list_before = context.indeed
    else:
        # to do
        pass

    data = get_data(context.path_to_ods)
    rejected_companies = []
    for i in range(1, len(data['Sheet1']) - 1):
        company = data['Sheet1'][i]
        if len(company) > 0:
            rejected_companies.append(company[0].lower())

    rejected_companies = list(set(rejected_companies))
    rejected_companies.sort()
    for i in range(len(list_before)):
        company = str(list_before[i][0]).lower()

        if company not in rejected_companies:
            list_updated.append(list_before[i])

    if source.lower() == 'indeed':
        context.indeed = list_updated
    else:
        # to do
        pass


@step('Docs API: Create HTML file with the found positions on "{source}"')
def create_html(context, source):
    assert source.lower() in ['indeed'], f"The resource should be 'Indeed', 'LinkedIn', 'ZipRecruiter', 'DICE'"

    data, days, location, radius = [], '1', 'remote', '25'
    if source.lower() == 'indeed':
        data = context.indeed
        days = context.indeed_days
        location = str(context.indeed_location).replace('%20', ' ').replace('%2C', ' ')
        radius = context.indeed_radius
    else:
        # to do
        pass

    today = date.today().strftime("%d-%m-%Y")
    file = context.path_to_html + f"Positions_for_applying_on_{source}_for_{today}.html"

    f = open(file, 'w')

    html_begin = f""" 
    <html> 
    <head>
    <style>
    th {{
      border: 1px solid black;
    }}
    td {{
      padding: 6px;
    }}    
    </style>
    </head> 
    <body> 
    <h2>Jobs posted on '{source}' within the past {days} days as of {today}</h2>
    <h4>Location: {location}</h4>
    <h4>Radius: {radius} miles</h4>
    <table>
    <tbody>    
    """
    f.write(html_begin)
    if len(data) < 1:
        row = f"<p style='color:red;'>Data not found on '{source}'</p>"
        f.write(row)
    else:
        row = f"<tr><th>#</th><th>Company</th><th>Job Title</th><th>Link</th></tr>"
        f.write(row)
        for i in range(len(data)):
            row = f"<tr><td>{i + 1}</td><td>{data[i][0]}</td><td>{data[i][1]}</td><td><a href='{data[i][2]}'>{data[i][2]}</a></td></tr>"
            f.write(row)

    html_close = """
    </tbody> 
    </table>  
    </body> 
    </html> 
    """
    f.write(html_close)
    f.close()

    context.last_created_html = file


@step('Docs API: Open created HTML file in the browser')
def open_html_file(context):
    webbrowser.open('file://' + context.last_created_html)


@step('Doc API: Generate the cover letter for the position "{position}" in company "{company}" for "{hiring_manager}"')
def make_cover_letter(context, position, company, hiring_manager):
    today = date.today().strftime("%m/%d/%Y")
    file_name = ('cover_letter_' + company.replace(' ', '_') + '_' + position.replace(' ', '_') + '_' +
                 today.replace('/', '_'))
    file_html = context.path_to_html + file_name + '.html'
    file_pdf = context.path_to_pdf + file_name + '.pdf'

    with open(context.cover_template) as ft:
        letter = ft.read()

    letter = (letter.replace('{today}', today).replace('{position}', position).
              replace('{company}', company).replace('{hiring_manager}', hiring_manager))

    f = open(file_html, 'w')
    f.write(letter)
    f.close()

    context.last_created_html = file_html
    converter.convert(f"file:///{file_html}", file_pdf)
    context.last_created_pdf = file_pdf


@step('Docs API: Open created PDF file in the browser')
def open_html_file(context):
    webbrowser.open('file://' + context.last_created_pdf)


@step('Docs API: Create HTML file with confirmations')
def create_html(context):
    confirmations = context.confirmations
    # confirmations = [['10/18/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software Test Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/18/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Sr Test Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/18/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software QA Tester', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/18/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Automated Test Engineer - US REMOTE or PA Office', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/17/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Automation Tester - API, Postman', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/17/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Senior System Level Test Engineer (SLT)', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/17/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software Quality Assurance Analyst III', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/17/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Sr Software Tester', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/17/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Test Automation Lead -(Federal agency)', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/16/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Python SDET', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/16/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Automated Test Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/15/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: QA Automation Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/13/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Test Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/13/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: QA Test Engineer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/13/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software Development Engineer - Test', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/12/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Python SDET', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/10/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Quality Assurance Automation Programmer', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/7/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Web SDET', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/7/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software Development Engineer in Test (SDeT)', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/7/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: SDET/QA Automation Engineer I', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['10/1/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: Software Engineer (REMOTE OPPORTUNITY)', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"], ['9/25/2023', 'Indeed Apply <indeedapply@indeed.com>', 'Indeed Application: IT Software Quality Assurance Testers @ Remote', "We'll help you get started \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c \u200c"]]
    file = context.path_to_html + f"Confirmations.html"

    f = open(file, 'w', encoding='utf-8')

    html_begin = f""" 
    <html> 
    <head>
    <style>
    th {{
      border: 1px solid black;
    }}
    td {{
      padding: 6px;
    }}    
    </style>
    </head> 
    <body> 
    <h2>Confirmations</h2>
    <table>
    <tbody>    
    """
    f.write(html_begin)
    if len(confirmations) < 1:
        row = f"<p style='color:red;'>No confirmations were found</p>"
        f.write(row)
    else:
        row = f"<tr><th>#</th><th>Date</th><th>From</th><th>Subject</th><th>Message</th></tr>"
        f.write(row)
        for i in range(len(confirmations)):
            r = confirmations[i]
            _from = r[1].replace('<', '(').replace('>',')')
            row = f"<tr><td>{i + 1}</td><td>{r[0]}</td><td>{_from}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
            f.write(row)

    html_close = """
    </tbody> 
    </table>  
    </body> 
    </html> 
    """
    f.write(html_close)
    f.close()

    context.last_created_html = file
