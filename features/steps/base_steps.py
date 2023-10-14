from behave import given, when, then, step


@step('The path to ODS file is {path}')
def set_path_to_ods(context, path):
    context.path_to_ods = path


@step('Looking for company "{company}"')
def set_variable(context, company):
    context.company = company


@step('The path to HTML file folder is {path}')
def set_path_to_html(context, path):
    context.path_to_html = path


@step('The path to PDF file folder is {path}')
def set_path_to_pdf(context, path):
    context.path_to_pdf = path


@step('The label for emails in Gmail is {gmail_label}')
def set_path_to_ods(context, gmail_label):
    context.gmail_label = gmail_label


@step('The cover template is {cover_template}')
def set_cover_template(context, cover_template):
    context.cover_template = cover_template


@step('Remove the positions that {condition} "{word}" in the job title from the list of found on "{source}"')
def update_found(context, condition, word, source):
    assert source.lower() in ['indeed'], f"The resource should be 'Indeed', 'LinkedIn', 'ZipRecruiter', 'DICE'"
    assert condition.lower() in ['do not have', 'have'], f"The condition should be 'have' or 'do not have'"

    list_before = []
    list_updated = []
    if source.lower() == 'indeed':
        list_before = context.indeed
    else:
        # to do
        pass

    for i in range(len(list_before)):

        if condition.lower() == 'do not have':

            if word.lower() in str(list_before[i][1]).lower():
                list_updated.append(list_before[i])

        elif condition.lower() == 'have':

            if word.lower() in str(list_before[i][1]).lower():
                continue
            else:
                list_updated.append(list_before[i])

    if source.lower() == 'indeed':
        context.indeed = list_updated
    else:
        # to do
        pass
