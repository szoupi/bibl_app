from django.views import generic, View
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required #for functions
from django.contrib.auth.mixins import PermissionRequiredMixin #for class
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Chapter, Verse, Annotation, FavoriteBook, FavoriteChapter, FavoriteVerse, FavoriteAnnotation, Profile
# Book uses generic view
from .forms import ChapterForm, VerseForm, AnnotationForm, UserRegistrationForm, UserLoginForm, ContactForm
import json
from django.core import serializers #for JSON
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from functions import continue_reading



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('bible:index')
    template_name = 'accounts/signup.html'


class PasswordResetView(View):
    success_url = reverse_lazy('bible:password_reset_done')
    template_name = 'registration/password_reset.html'

# TODO
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# BOOK INDEX page: display books as list
class IndexView(generic.ListView):
    model = Book
    template_name = 'bible/index.html'

    # return all book objects from the db
    # it returns a var called object_list
    # with a list of the objects (books)
    # but we can override it with 
    #context_object_name = 'my_variable'
    context_object_name = 'all_books'

    def get_queryset(self):
        return Book.objects.all()
        # limit objects to 2
        # return Book.objects.all()[:2]


# BOOK DETAIL page: display details about one object (book)
def book_detail_view(request, book_id):
    # use
    book = get_object_or_404(Book, pk=book_id)
    user = request.user.id
    # first does not produce error if row does not exists
    favorite = FavoriteBook.objects.filter(obj_id=book_id, user=user).first()

    # save current path
    continue_reading(request)

    # the context {'book':book} contain the variables passed to template
    return render(request, 'bible/book_detail.html', {
        'book': book,
        'favorite': favorite,
    })

    # model = Book
    # template_name = ""
    # context_object_name = 'all_books'

def book_abstract_trempelas_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user.id
    # first does not produce error if row does not exists
    favorite = FavoriteBook.objects.filter(obj_id=book_id, user=user).first()
    favorite_chapters = FavoriteChapter.objects.all()

    return render(request, 'bible/book_abstract_trempelas.html',{
        'book': book,
        'favorite': favorite,
        'favorite_chapters': favorite_chapters
    })

#####################################################
# CREATE BOOKS
# class for creating books using fMODEL FORMS in front end


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'bible.add_book'
    #what object do you create?
    model = Book
    #what template to use?
    template_name = 'bible/book_form.html'

    #what fields do you want to use in the form?
    # select them from the models.py
    # add url pattern too in urls.py
    fields = ['title', 'writer', 'image', 'abstract_trempelas', 'notes']
    
#####################################################
# CREATE CHAPTERS
# book_id is the parameter passed from the url pattern 
# #/bible/book_id/
#'pk' (aka primary key), or 'id' variable is automatic understandble by django

@login_required
@permission_required('bible.add_chapter')
def create_chapter(request, book_id):
    cBook = get_object_or_404(Book, pk=book_id)

    # If this is a POST request, then process the Form data
    # and redirect to book details
    if request.method == 'POST':
        # Create a form instance from forms.py and 
        # populate it with data from the request (binding):
        form = ChapterForm(request.POST)

        if form.is_valid():
            # save the form data to db
            form.save()
            
            return render(request, 'bible/book_detail.html', {
                'book': cBook,  # return object
            })


    # If this is a GET (or any other method) 
    # aka user just request an empty form
    # 1. create the default form,
    # 2. assign book_id to book model (FK) field (initiall...)
    # 3. stay in the same template
    else:
        form = ChapterForm(initial = {
            'book' : book_id,
        })

    return render(request, 'bible/chapter_form.html', {
        'book': cBook,  # return object
        'form': form
    })
#####################################################
# CREATE VERSES
# chapter_id are the parameters passed from the url pattern 
# bible/book/id/chapter/id/verse/add

@login_required
@permission_required('bible.add_verse')
def create_verse(request, book_id, chapter_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)

    if request.method == 'POST':
        form = VerseForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, 'bible/chapter_detail.html', {
                'book': book,
                'chapter': chapter
            })
    else:
        form = VerseForm(initial = {
            'chapter': chapter_id,
        })
    
    return render(request, 'bible/verse_form.html', {
        'book': book,
        'chapter': chapter,
        'form': form
    })

#####################################################
# CREATE ANNOTATION
# verse_id are the parameters passed from the url pattern
# bible/verse/id/annotation/add

@login_required
@permission_required('bible.add_annotation')
def create_annotation(request, book_id, chapter_id, verse_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    verse = get_object_or_404(Verse, pk=verse_id)

    if request.method == 'POST':
        form = AnnotationForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, 'bible/verse_detail.html', {
                'book': book,
                'chapter': chapter,
                'verse': verse
            })
    else:
        form = AnnotationForm(initial={
            'verse': verse_id,
        })

    return render(request, 'bible/annotation_form.html', {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'form': form
    })
#####################################################
# DETAIL VIEWS
def chapter_detail_view(request, book_id, chapter_id):
    book = Book.objects.get(pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    user = request.user.id
    favorite = FavoriteChapter.objects.filter(
        obj_id=chapter_id, user=user).first()
    favorite_verses = FavoriteVerse.objects.all()
    
    # save current path
    continue_reading(request)

    # assert False
    return render(request, 'bible/chapter_detail.html', {
        'book': book,
        'chapter': chapter,
        'favorite': favorite,
        'favorite_verses': favorite_verses
    })



def verse_detail_view(request, book_id, chapter_id, verse_id):
    book = Book.objects.get(pk=book_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    verse = get_object_or_404(Verse, pk=verse_id)
    user = request.user.id
    favorite = FavoriteVerse.objects.filter(obj_id=verse_id, user=user).first()
    favorite_annotations = FavoriteAnnotation.objects.all()

    # save current path 
    continue_reading(request)

    return render(request, 'bible/verse_detail.html', {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'favorite': favorite,
        'favorite_annotations': favorite_annotations
    })


def annotation_detail_view(request, annotation_id):
    annotation = get_object_or_404(Annotation, pk=annotation_id)
    user = request.user.id
    favorite = FavoriteVerse.objects.filter(
        obj_id=annotation_id, user=user).first()

    return render(request, 'bible/annotation_detail.html', {
        'annotation': annotation,
        'favorite': favorite
    })

#####################################################
# UPDATE VIEWS


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required='bible.change_book'
    model = Book
    fields = ['title', 'writer', 'image', 'abstract_trempelas', 'notes']
    template_name = 'bible/book_form.html'

@login_required
@permission_required('bible.change_chapter')
def Chapter_Update(request, book_id, chapter_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    form = ChapterForm(request.POST or None, instance=chapter)
    if form.is_valid():
        form.save()
        return render(request, 'bible/book_detail.html', {
            'book': book
        })
    return render(request, 'bible/chapter_form.html', {'form': form})

@login_required
@permission_required('bible.change_verse')
def Verse_Update(request, book_id, chapter_id, verse_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    verse = Verse.objects.get(pk=verse_id)
    form = VerseForm(request.POST or None, instance=verse)
    if form.is_valid():
        form.save()
        return render(request, 'bible/chapter_detail.html', {
            'book': book,
            'chapter': chapter
        })
    return render(request, 'bible/verse_form.html', {'form': form})


@login_required
@permission_required('bible.change_annotation')
def Annotation_Update(request, book_id, chapter_id, verse_id, annotation_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    verse = get_object_or_404(Verse, pk=verse_id)
    annotation = Annotation.objects.get(pk=annotation_id)
    form = AnnotationForm(request.POST or None, instance=annotation)
    if form.is_valid():
        form.save()
        return render(request, 'bible/verse_detail.html', {
            'book': book,
            'chapter': chapter,
            'verse': verse
        })
    return render(request, 'bible/annotation_form.html', {'form': form})
    

#####################################################
# DELETE VIEWS
class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'bible.delete_book'
    model = Book
    success_url = reverse_lazy('bible:index')
    template_name = 'bible/book_confirm_delete.html'


# TODO add confirmation dialogs
@login_required
@permission_required('bible.delete_chapter')
def Chapter_Delete(request, book_id, chapter_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    chapter.delete()
    return render(request, 'bible/book_detail.html', {
        'book': book,
        'chapter': chapter
    })

@login_required
@permission_required('bible.delete_verse')
def Verse_Delete(request, book_id, chapter_id, verse_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    verse = Verse.objects.get(pk=verse_id)
    verse.delete()
    return render(request, 'bible/chapter_detail.html', {
        'book': book,
        'chapter': chapter,
        'verse': verse
    })

@login_required
@permission_required('bible.delete_annotation')
def Annotation_Delete(request, book_id, chapter_id, verse_id, annotation_id):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    verse = get_object_or_404(Verse, pk=verse_id)
    annotation = Annotation.objects.get(pk=annotation_id)
    annotation.delete()
    return render(request, 'bible/verse_detail.html', {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'annotation': annotation
    })


# class UserRegistrationView(View):
#     form_class = UserRegistrationForm
#     template_name = 'registration/registration_form.html'

#     # built in functions for GET/POST requests
#     # display blank form, None is the context
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {
#             'form': form
#         })

#     def post(self, request):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             # create user object from data, but not save it yet to db
#             user = form.save(commit=False)

#             # cleaned (normalized) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()

#             # return user objects if credentials are correct
#             user = authenticate(username=username, password=password)

#             # check if user is already registered
#             if user is not None:

#                 if user.is_active:
#                     login(request, user)
#                     return redirect('bible:index')
        
#         return render(request, self.template_name, {
#             'form': form
#         })


class populateQuickAccessBooksView(View):
    ''' populate the dropdown boxes async
    with books, chapters and verses
    fetched as json
    '''
    def get(self, request):
        # https://stackoverflow.com/questions/12553599/create-json-response-in-django-with-model?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        # https://docs.djangoproject.com/en/1.9/topics/serialization/
        data = {
            'fetchedBooks': serializers.serialize('json', Book.objects.all()),
        }
        return JsonResponse(data)


class populateQuickAccessChaptersView(View):

    def get(self, request):
        # selected_book = request.GET.get('selected_book')
        data = {
            'fetchedChapters': serializers.serialize('json', Chapter.objects.all()),
        }

        return JsonResponse(data)


class populateQuickAccessVersesView(View):

    def get(self, request):
        data = {
            'fetchedVerses': serializers.serialize('json', Verse.objects.all()),
        }

        return JsonResponse(data)

# FAVORITES one view for books, chapters etc
class FavoriteView(LoginRequiredMixin, View):
    # This variable will set the favorite model to be processed
    # model = FavoriteBook
    # model is set on the url
    model = None

    def put(self, request, pk):
        # We need a user
        user = auth.get_user(request)

        # Trying to get a favorite from the table, or create a new one
        # The first element is an instance of the model 
        # you are trying to retrieve 
        # and the second is a boolean flag to tell 
        # if the instance was created or not. 
        # True means the instance was created by the get_or_create method 
        # and False means it was retrieved from the database.
        favorite, created = self.model.objects.get_or_create(
            user=user, 
            obj_id=pk)
        # If no new favorite has been created,
        # Then we believe that the request was to delete the favorite
        if not created:
            favorite.delete()

            # pass some data to be used 
            # in the fetch promise
            # not necessary needed 
            # data = {
            #     "result": created,
            #     "object_is_favorited": True,
            # }
            data={}

            return JsonResponse(data)

    def get(self, request, pk):
        user = auth.get_user(request)
        favorite = self.model.objects.get(user=user, obj_id=pk)
        if favorite.DoesNotExist:
            return JsonResponse({
                'success': 0
            })
        else:
            return JsonResponse({
                'success': 1
            })


class DisplayFavoritesView(LoginRequiredMixin, View):
    # one model must be set TODO: really? test it
    # model = FavoriteBook

    context_object_name = 'fav_books'
    template_name = 'bible/favorites.html'

    # pass multiple models to template
    def get_context_data(self, **kwargs):
        context = super(DisplayFavoritesView, self).get_context_data(**kwargs)
        return context

    def get(self, request):
        user = auth.get_user(request)
        
        # Query: From chapters select those that appear on favorite chapter and belong to current user
        # (To refer to a reverse relationship, just use the lowercase name of the model)
        favorite_books = Book.objects.filter(favoritebook__user=request.user)

        # another method to filter join two queries
        # fav_books_list = FavoriteBook.objects.filter(user=request.user)
        # fav_books = Book.objects.filter()
        # filter fav_books on subquery fav_books_list
        # fav_books.query.__dict__ = fav_books_list.query.__dict__

        favorite_chapters = Chapter.objects.filter(favoritechapter__user=request.user)

        # reverse lookup to get the book id 
        # in template use {{verse.chapter.book}}
        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#django.db.models.query.QuerySet.select_related
        favorite_verses = Verse.objects.select_related(
            'chapter__book').filter(favoriteverse__user=request.user)
        favorite_annotations = Annotation.objects.select_related(
            'verse__chapter__book').filter(favoriteannotation__user=request.user)


        return render(request, 'bible/favorites.html', {
            'favorite_books': favorite_books,
            'favorite_chapters': favorite_chapters,
            'favorite_verses': favorite_verses,
            'favorite_annotations': favorite_annotations
        })

# --------- Search --------------------------------------------
# search books, chapters, verses, annotations content
class SearchView(View):
    
    # pass multiple models to template
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return context

    def get(self, request):
        # q varilable is passed from the form
        if 'q' in request.GET and request.GET['q']:
            query = request.GET['q']
            books_filtered = Book.objects.filter(
                Q(title__icontains=query) | Q(abstract_trempelas__icontains=query))
            chapters_filtered = Chapter.objects.filter(
                Q(title__icontains=query) | Q(abstract_trempelas__icontains=query))
            verses_filtered = Verse.objects.filter(
                Q(original_text__icontains=query) | Q(greek_translation__icontains=query))
            annotations_filtered = Annotation.objects.filter(annotation__icontains=query)
            # message = 'You searched for: %r' % request.GET['q']

            return render(request, 'bible/search.html', {
                'books_filtered': books_filtered,
                'chapters_filtered': chapters_filtered,
                'verses_filtered': verses_filtered,
                'annotations_filtered': annotations_filtered,
                'query': query,
            })

        else:
            return render(request, 'bible/search.html')

# --------- DASHBOARD --------------------------------------------


class DashboardView(View):
    
    template_name = "bible/dashboard.html"

    # pass multiple models to template
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

    def get(self, request):
        user = auth.get_user(request)
        
        if Profile.objects.filter(user=user).exists():
            p = Profile.objects.get(user=user)
            continue_reading_url = p.continue_reading_url
            return render(request, 'bible/dashboard.html', {
                'continue_reading_url': continue_reading_url
            })
        else:
            return render(request, 'bible/dashboard.html', {

            })


# --------- send email form --------------------------------------------
def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            # gmail overrides from_email option with EMAIL_HOST_USER
            from_email = form.cleaned_data['from_email']
            recipient_list = ['szoupi@gmail.com']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['name'] + '\n'
            message += form.cleaned_data['email'] + '\n'
            message += form.cleaned_data['team'] + '\n'
            message += form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/success')
    return render(request, "bible/email.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your  message.')

# --------- end send email form -----------------------------------------
