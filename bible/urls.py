from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .import views
from django.views.generic import TemplateView 
from django.conf.urls import include
from .models import FavoriteBook, FavoriteChapter, FavoriteVerse, FavoriteAnnotation

app_name = 'bible'

urlpatterns = [
    # BIBLE LIST VIEW (INDEX)
    #/bible/ 
    url(r'^$', views.IndexView.as_view(), name='index'),

    # put  service-worker.js in the root of templates directory
    url(r'^sw.js', (TemplateView.as_view(template_name="sw.js",
                                         content_type='application/javascript', )), name='sw.js'),
    # AUTHENTICATE django defaults names and paths
    # accounts/login/ 
    # accounts/logout/

    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/bible/login'}, name='logout'),
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),

    # TODO BUG
    # https://code.i-harness.com/en/q/135de11

    # #override the default urls
    # url(r'^password/change/$',
    #     auth_views.password_change,
    #     name='password_change'),
    # url(r'^password/change/done/$',
    #     auth_views.password_change_done,
    #     name='password_change_done'),
    # url(r'^password/reset/$',
    #     auth_views.password_reset,  {'template_name': 'registration/password_reset_form.html'},
    #     name='password_reset'),
    # url(r'^password/reset/done/$',
    #     auth_views.password_reset_done, {
    #         'template_name': 'registration/password_reset_done.html'},
    #     name='password_reset_done'),
    # url(r'^password/reset/complete/$',
    #     auth_views.password_reset_complete,
    #     name='password_reset_complete'),
    # url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     auth_views.password_reset_confirm,
    #     name='password_reset_confirm'),


    # ADD (CREATE) VIEW ###########################################################

    # BIBLE ADD
    # bible/book/add
    # no id is needed, it is auto generated
    url(r'^book-create/$', views.BookCreate.as_view(), name='book-add'),

    # CHAPTER ADD
    # bible/book/id/chapter/create-chapter
    # no id is needed, it is auto generated
    url(r'^book/(?P<book_id>[0-9]+)/create-chapter/$',
        views.create_chapter, name='chapter-create'),

    # VERSE ADD
    # bible/book/chapter/id/verse/create-verse
    # no verse id is needed, it is auto generated
    # no book_id is needed, because verse is child of a unique chapter (id)
    # and not a combination of book and chapter
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/create-verse/$',
        views.create_verse, name='verse-create'),

    # ANNOTATION ADD
    # bible/verse/id/annotation/create-annotation
    # no annotation id is needed, it is auto generated
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)/create-annotation/$',
        views.create_annotation, name='annotation-create'),

    # DETAILS VIEW ###########################################################

    # BOOK DETAILS  /bible/id/
    # childeren CHAPTERS are displayed as list
    url(r'^book/(?P<book_id>[0-9]+)$',
        views.book_detail_view, name='book-detail'),

    # CHAPTER DETAIL  bible/book_id/chapter/chapter_id
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)$',
        views.chapter_detail_view, name='chapter-detail'),

    # VERSE DETAIL 
    # bible/book_id/chapter/chapter_id/verse/verse_id
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)$',
        views.verse_detail_view, name='verse-detail'),
    
    # ANNOTATION DETAIL VIEW : needed for favorites page link??
    # bible/chapter/annotation_id
    url(r'^annotation/(?P<annotation_id>[0-9]+)$',
        views.annotation_detail_view, name='annotation-detail'),

    # UPDATE, DELETE VIEW ###########################################################
    
    # BOOK UPDATE /bible/id/update
    # we don't use the word 'book' before the id to shorten url
    url(r'^(?P<pk>[0-9]+)/update/$',
        views.BookUpdate.as_view(), name='book-update'),
    
    # BOOK DELETE /bible/id/delete
    url(r'^(?P<pk>[0-9]+)/delete/$',
        views.BookDelete.as_view(), name='book-delete'),

    # CHAPTER UPDATE /bible/book_id/chapter/chapter_id/update/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/update/$',
        views.Chapter_Update, name='chapter-update'),

    # CHAPTER DELETE /bible/book_id/chapter/chapter_id/delete/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/delete/$',
        views.Chapter_Delete, name='chapter-delete'),

    # VERSE UPDATE /bib/chapter/chapter_id/verse/verse_id/update/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)/update/$',
        views.Verse_Update, name='verse-update'),

    # VERSE DELETE /bible/chapter/chapter_id/rse/idverse_/delete/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)/delete/$',
        views.Verse_Delete, name='verse-delete'),

    # ANNOTATION UPDATE /bible/verse/verse_id/annotation/id/update/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)/annotation/(?P<annotation_id>[0-9]+)/update/$',
        views.Annotation_Update, name='annotation-update'),
    # ANNOTATION DELETE /bible/verse/verse_id/annotation/id/delete/
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)/annotation/(?P<annotation_id>[0-9]+)/delete/$',
        views.Annotation_Delete, name='annotation-delete'),


    # FAVORITE  ###########################################################

    # BOOK  /bible/book/id/favorite
    # define the model because the view is general
    url(r'^book/(?P<pk>[0-9]+)/favorite/$',
        views.FavoriteView.as_view(model=FavoriteBook), name='book-favorite'),

    # CHAPTER  /bible/chapter/id/favorite
    # define the model because the view is general
    url(r'^chapter/(?P<pk>[0-9]+)/favorite/$',
        views.FavoriteView.as_view(model=FavoriteChapter), name='chapter-favorite'),

    # VERSE  /bible/verse/id/favorite
    # define the model because the view is general
    url(r'^verse/(?P<pk>[0-9]+)/favorite/$',
        views.FavoriteView.as_view(model=FavoriteVerse), name='verse-favorite'),

    # ANNOTATION  /bible/annotation/id/favorite
    # define the model because the view is general
    url(r'^annotation/(?P<pk>[0-9]+)/favorite/$',
        views.FavoriteView.as_view(model=FavoriteAnnotation), name='annotation-favorite'),

    # USER FAVORITES  /bible/favorites
    # define the model because  the view is general
    # TODO: TEST IF MODEL CAN BE OMITTED IN THIS CASE
    url(r'^favorites/$',
        views.DisplayFavoritesView.as_view(), name='favorites'),


]

# if settings.DEBUG:
#     urlpatterns += [url(r'^debuginfo/$', views.debug), ]
