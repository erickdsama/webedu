from django.conf.urls import url
from .views import ImportarCreateView, ProcesarImportacionView, DownloadFormatView

urlpatterns = [
    url(r'^importar-archivo/$', ImportarCreateView.as_view(), name='importar-archivo'),
    url(r'^procesar-importacion/(?P<pk>\d+)/$', ProcesarImportacionView.as_view(), name='procesar-importacion'),
    url(r'^descargar-formato/$', DownloadFormatView.as_view(), name='descargar-formato'),
]