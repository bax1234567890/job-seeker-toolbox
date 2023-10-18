from behave import given, when, then, step
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import os
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#
import datetime


# If modifying these scopes, delete the file gmail_token.json.
SCOPES = ['https://mail.google.com/']


def gmail_authenticate_behave():
    creds = None
    # The file gmail_token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gmail_token.json'):
        creds = Credentials.from_authorized_user_file('gmail_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gmail_token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def search_email_ids_by_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    email_ids = []
    if 'messages' in result:
        email_ids.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            email_ids.extend(result['messages'])
    return email_ids


@step('Gmail API: Verify if "{query}" {condition} exist in emails')
def is_message_in_email(context, query, condition):
    assert condition in ['should', 'should not'], f"The condition must be 'should' or 'should not'"
    if query == 'company':
        query = context.company

    try:
        # Call the Gmail API
        service = gmail_authenticate_behave()

        email_ids = search_email_ids_by_messages(service, query=context.gmail_label + ' ' + query)
        if email_ids and condition == 'should':
            print(email_ids)

            for i in range(len(email_ids)):
                email = service.users().messages().get(userId='me', id=email_ids[i]['id'], format='full').execute()
                print(f"--- {i + 1} ---\n" + email['snippet'])

        elif email_ids and condition == 'should not':
            raise ValueError(f"I have already interacted with {query}")

        elif not email_ids and condition == 'should not':
            print(f"I have never interacted with {query}")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


@step('Gmail API: Remove the positions that have already been applied for from the list of found on "{source}"')
def update_found(context, source):
    assert source.lower() in ['indeed'], f"The resource should be 'Indeed', 'LinkedIn', 'ZipRecruiter', 'DICE'"

    list_before = []
    list_updated = []
    if source.lower() == 'indeed':
        list_before = context.indeed
    else:
        # to do
        pass

    service = gmail_authenticate_behave()

    for i in range(len(list_before)):
        company = str(list_before[i][0]).lower()
        email_ids = search_email_ids_by_messages(service, query=context.gmail_label + ' ' + company)
        if not email_ids:
            list_updated.append(list_before[i])

    if source.lower() == 'indeed':
        context.indeed = list_updated
    else:
        # to do
        pass


@step('Gmail API: Get a list of application confirmations from "{source}"')
def get_confirmations(context, source):
    def get_value_from_headers(data, header_name):
        _headers = data['payload']['headers']
        for i in range(len(_headers)):
            if _headers[i]['name'] == header_name:
                return _headers[i]['value']
        return ''

    def get_date(data):
        epoch_time = str(data['internalDate'])
        epoch_time = int(epoch_time[0:len(epoch_time) - 3])
        return datetime.datetime.fromtimestamp(epoch_time)

    confirmations = []
    label = context.gmail_label
    if source.lower() == 'indeed':
        label = label + ' ' + 'indeedapply@indeed.com'
    elif source.lower() == 'amazon':
        label = label + ' ' + 'noreply@mail.amazon.jobs'
    elif source.lower() == 'worksourcewa':
        label = label + ' ' + 'WorkSourceWashingtonNoReply@esd.wa.gov'

    service = gmail_authenticate_behave()
    email_ids = search_email_ids_by_messages(service, query=label)

    for i in range(len(email_ids)):
        email = service.users().messages().get(userId='me', id=email_ids[i]['id'], format='full').execute()

        _date = get_date(email)
        # {email_date.month}/{email_date.day}/{email_date.year}
        email_date = f"{_date.month}/{_date.day}/{_date.year}"
        email_from = get_value_from_headers(email, 'From')
        email_subject = get_value_from_headers(email, 'Subject')
        email_snippet = str(email['snippet']).replace('&#39;', '\'').replace('&amp;', '&')

        confirmations.append([email_date, email_from, email_subject, email_snippet])

    context.confirmations = confirmations

