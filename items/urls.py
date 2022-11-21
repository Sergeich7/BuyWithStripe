from django.urls import path
from django.http import HttpResponse

from .views import session_to_json
from .views import ProdDetailView, IndexListView

app_name = 'items'
urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('item/<str:pk>', ProdDetailView.as_view(), name='detail'),
    path('buy/<str:pk>', session_to_json, name='buy'),
    path('success/', lambda request : HttpResponse('Платёж выполнен'), name='success'),
    path('cancel/', lambda request : HttpResponse('Ошибка: платёж не прошел'), name='cancel'),
]
