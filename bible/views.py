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
from .models import Book, Chapter, Verse, Annotation, FavoriteBook
# Book uses generic view
from .forms import ChapterForm, VerseForm, AnnotationForm, UserRegistrationForm, UserLoginForm
import json
from django.http import HttpResponse

# TODO
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# BOOK INDEX page: display books as list
class IndexView(generic.ListView):
    model = Book
    template_name = 'bible/index.html'
    # queryset = Book.object.filter(title__icontains='mysearch')[:5] # Get 5 books containing the title mysearch

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
    # the context {'book':book} contain the variables passed to template
    return render(request, 'bible/book_detail.html', {
        'book': book,
    })

    # model = Book
    # template_name = ""
    # context_object_name = 'all_books'

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
    # assert False
    return render(request, 'bible/chapter_detail.html', {
        'book': book,
        'chapter': chapter
    })


def verse_detail_view(request, book_id, chapter_id, verse_id):
    book = Book.objects.get(pk=book_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    verse = get_object_or_404(Verse, pk=verse_id)
    return render(request, 'bible/verse_detail.html', {
        'book': book,
        'chapter': chapter,
        'verse': verse
    })

def annotation_detail_view(request, annotation_id):
    annotation = get_object_or_404(Annotation, pk=annotation_id)
    return render(request, 'bible/annotation_detail.html', {
        'annotation': annotation
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


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'registration/registration_form.html'

    # built in functions for GET/POST requests
    # display blank form, None is the context
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # create user object from data, but not save it yet to db
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return user objects if credentials are correct
            user = authenticate(username=username, password=password)

            # check if user is already registered
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('bible:index')
        
        return render(request, self.template_name, {
            'form': form
        })

# FAVORITES
class FavoriteView(LoginRequiredMixin, View):
    # This variable will set the favorite model to be processed
    model = None

    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a favorite from the table, or create a new one
        favorite, created = self.model.objects.get_or_create(
            user=user, obj_id=pk)
        # If no new favorite has been created,
        # Then we believe that the request was to delete the favorite
        if not created:
            favorite.delete()


        return HttpResponse(
            json.dumps({
                "result": created,
                "book_is_favoriteed": True,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )



    # def get_favorite_count(self, request, pk):
    #     user = auth.get_user(request)
    #     favorite = self.model.objects.get(user=user, obj_id=pk)
    #     count = favorite.count()
    #     return count


# class LoginView(View):
#     form_class = UserLoginForm
#     template_name = 'bible/login_form.html'

#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {
#             'form': form
#         })

#     def post(self, request):
#         print(request.user.is_authenticated())
#         next = request.GET.get('next')
#         form = self.form_class(request.POST)

#         if form.is_valid():

#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     print('user is active')
#                     login(request, user)
#                     if next:
#                         return redirect(next)
#                     return redirect('/')
#                 else:
#                     print('user is disabled')
#                     return render(request, 'bible/login_form.html', {
#                         'error_message': 'Your account has been disabled',
#                         'form': form
#                     })
#             else:
#                 print('user is active')
#                 return render(request, 'bible/login_form.html', {
#                     'error_message': 'Invalid login',
#                     'form': form
#                     })
#             print('form is valid only')
#         return redirect('/')


# def logout_view(request):
#     logout(request)
#     return redirect('/')


# def login_user(request):
#     form_class = UserLoginForm
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # books = Book.objects.filter(user=request.user)
#                 return render(request, 'bible/index.html')
#             else:
#                 return render(request, 'bible/login_form.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'bible/login_form.html', {'error_message': 'Invalid login'})
#     return render(request, 'bible/login_form.html')
