from pyexcel_ods3 import get_data
from behave import given, when, then, step
from datetime import date
import webbrowser


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
    file = context.path_to_html+f"Positions_for_applying_on_{source}_for_{today}.html"

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
            row = f"<tr><td>{i+1}</td><td>{data[i][0]}</td><td>{data[i][1]}</td><td><a href='{data[i][2]}'>{data[i][2]}</a></td></tr>"
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
    webbrowser.open(context.last_created_html)
