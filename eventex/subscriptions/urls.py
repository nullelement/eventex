from django.conf.urls import url
from eventex.subscriptions.views import new, detail

urlpatterns = [
    url(r'^$', new, name='new'),
    url(r'^(\d+)/$', detail, name='detail'), # (\d+) Significa um ou mais dígitos que esse cara seja capturado. Vai ser passado como argumento para a view detail.
]
