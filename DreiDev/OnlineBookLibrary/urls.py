from django.conf.urls import url
from django.contrib.auth import views as auth_views
from OnlineBookLibrary.views import(
    HomeView, UserRegisteration, LibraryCreation,
    LibraryList, LibraryView, BookCreate
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^user/new/$', UserRegisteration.as_view(), name='user-new'),
    url(r'^user-login/$', auth_views.login, name='user-login'),
    url(
        r'^user-logout/$', auth_views.logout,
        {'next_page': '/onlinebooklibrary/'}, name='user-logout'),
    url(r'^library/new/$', LibraryCreation.as_view(), name='library-new'),
    url(r'^library/list/$', LibraryList.as_view(), name='library-list'),
    url(
        r'^library/(?P<slug>[\w\-]+)/$',
        LibraryView.as_view(), name='library-detail'),
    url(
        r'^library/(?P<slug>[\w\-]+)/book-create/$',
        BookCreate.as_view(), name='book-create'),
]
