from django.urls import path
from .views import *


urlpatterns= [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('signout/', signout, name='signout'),
    # path('entry/', entry, name='entry'),
    # path('entry/<int:entry_id>/', entry_get, name='entry_get'),
    # path('entry/delete/<int:entry_id>/', entry_delete, name='entry_delete'),
    # path('entry_put/<int:entry_id>/', entry_put, name='entry_put'),
    # path('deleteds/', Deleteds.as_view(), name='deleteds'),
    # path('signin/', UserLoginView.as_view()),
    ]