# First stab at writing the view functions
# STOP! DO NOT write production code like this.
# There is a better way!

from django.http import HttpResponse
from models import Entry


def entries_list(request):
    '''List all the blog entries'''
    all_entries = Entry.objects.all()
    entry_row = '''
        <tr>
            <td><a href = "./%(id)s"> %(title)s </a></td>
            <td> %(dt)s </td>
        </tr>'''
    table_rows = [entry_row % {'id': entry.id,
                               'title': entry.title,
                               'dt': entry.date_created}
                  for entry in all_entries]
    page = '''
        <!DOCTYPE html>
        <html>
            <head>
                <title> All entries </title>
            </head>
            <body>
                <table>
                    <tr>
                        <th> Title </th>
                        <th> Date </th>
                    </tr>
                %s
                </table>
            </body>
        </html>''' % '\n'.join(table_rows)

    return HttpResponse(page)