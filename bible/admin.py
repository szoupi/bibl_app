from django.contrib import admin
from models import Book, Chapter, Verse, Annotation

#default way
#admin.site.register(Annotation)

# Define the class for the admin interface
class ChapterAdmin(admin.ModelAdmin):
    #display objects horizontaly (list)
    list_display = ('book', 'number', 'title')
    #display filter panel
    list_filter = ('book', 'number')
    
    # DETAIL VIEW
    #display horizontaly and change the order
    # fields = [('number', 'title'), 'book']
    # hide fields
    #exclude = ['book']

# Register the admin class with the associated model
admin.site.register(Chapter,ChapterAdmin)

# ALTERNATIVE ADMIN REGISTRATION
# Register the Admin classes for Book using the @register decorator 
# to register the models (this does exactly the same thing 
# as the admin.site.register() syntax)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'id')


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('original_text', 'chapter', 'number', 'id')

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('number', 'phrase', 'annotation', 'verse_id')
