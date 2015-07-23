from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^subscribe$', Subscribe.as_view(), name='subscribe'),
    url(r'^unsubscribe$', Unsubscribe.as_view(), name='unsubscribe'),
    url(r'^subscribed$', Subscribed.as_view(), name='subscribed'),
    url(r'^cleaned$', UpdateCleaned.as_view(), name='cleaned'),
    url(r'^resubscribe-cleaned$', ResubscribeCleaned.as_view(), name='resubscribe-cleaned'),
]