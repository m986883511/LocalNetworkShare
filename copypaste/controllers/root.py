import json

from pecan import expose, render, request
from webob.exc import status_map


class Share:
    value = ''


class RootController(object):

    @expose(generic=True)
    def index(self):
        return render('index.html', dict(share_value=Share.value))

    @index.when(method='POST')
    def index_post(self, q):
        Share.value = q
        # redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)
        return dict()

    @expose()
    def share_value(self):
        if request.method == 'POST':
            value = json.loads(request.body)
            Share.value = value.get('value')
        else:
            return Share.value

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
