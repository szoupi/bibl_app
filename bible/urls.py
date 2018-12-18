from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .import views
from django.views.generic import TemplateView 
from django.conf.urls import include
from .models import Book, Chapter, Verse, FavoriteBook, FavoriteChapter, FavoriteVerse, FavoriteAnnotation

app_name = 'bible'

urlpatterns = [
    # BIBLE LIST VIEW (INDEX)
    #/bible/ 
    url(r'^$', views.IndexView.as_view(), name='index'),

    # put  service-worker.js in the root of templates directory
    url(r'^sw.js', (TemplateView.as_view(template_name="sw.js",
        content_type='application/javascript', )), name='sw.js'),

    
    # AUTHENTICATE django defaults names and paths
    # django.contrib.auth.urls is needed here for login logout views
    # it is also used on annotations/urls.py
    url('', include('django.contrib.auth.urls')),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/password_change_done'}, name='logout'),
    url('^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'password_change/$', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html', success_url='/accounts/password_change_done')),
    url(r'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
    url(r'password_reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html',
                                                                  subject_template_name='password_reset_subject.txt', success_url='/accounts/password_reset_done/', from_email='szoupi@gmail.com')),
    url(r'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')),
    url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', success_url='/accounts/password_reset_complete/')),
    url(r'password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html')),




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

    url(r'^book/(?P<book_id>[0-9]+)/abstract$',
        views.book_abstract_trempelas_view, name='book-abstract-trempelas'),

    # CHAPTER DETAIL  bible/book_id/chapter/chapter_id
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)$',
        views.chapter_detail_view, name='chapter-detail'),

    # VERSE DETAIL 
    # bible/book_id/chapter/chapter_id/verse/verse_id
    url(r'^book/(?P<book_id>[0-9]+)/chapter/(?P<chapter_id>[0-9]+)/verse/(?P<verse_id>[0-9]+)$',
        views.verse_detail_view, name='verse-detail'),
    
    # ANNOTATION DETAIL VIEW
    # bible/chapter/annotation_id
    # url(r'^annotation/(?P<annotation_id>[0-9]+)$',
    #     views.annotation_detail_view, name='annotation-detail'),

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
    
    
    # POPULATE DROPDOWN INPUTS  #####################################################

    # POPULATE QUICK ACCESS
    # /bible/populate/books
    url(r'^populate/books/$',
        views.populateQuickAccessBooksView.as_view(), name='populate-books'),

    # /bible/populate/chapters
    url(r'^populate/chapters/$',
        views.populateQuickAccessChaptersView.as_view(), name='populate-chapters'),

    # /bible/populate/chapters
    url(r'^populate/verses/$',
        views.populateQuickAccessVersesView.as_view(), name='populate-verses'),

    # send email form
    url(r'^email/$',
        views.emailView, name='email-send'),
    url(r'^success/$',
        views.successView, name='email-success'),
]

# if settings.DEBUG:
#     urlpatterns += [url(r'^debuginfo/$', views.debug), ]
