from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import Truncator
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=250, blank = False)
    writer = models.CharField(max_length=160)
    #/media/default.jpg
    image = models.FileField(default='/default.jpg')
    abstract_trempelas = models.TextField()
    notes = models.TextField()

    def get_absolute_url(self):
        # return the pk of the current object book
        # from the url
        #eg /book/1
        # returns a URL for displaying individual model records on the website
        # (if you define this method then Django will automatically add
        # a "View on Site" button to the model's record
        # editing screens in the Admin site)
        return reverse('bible:book-detail', kwargs={
            'book_id': self.pk})

    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    abstract_trempelas = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def get_absolute_url(self):
        # return the pk of the current chapter
        # from the url
        #eg /book/book_id/chapter/chapter_id
        return reverse('bible:chapter-detail', kwargs={
            'book_id': self.book,
            'chapter_id': self.pk
        })

    def __unicode__(self):
        return u'%s %s' % (self.number, self.title)


class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT)
    number = models.CharField(max_length=10)
    original_text = models.TextField(
        max_length=1000, help_text='Ancient Greek script')
    greek_translation = models.TextField(
        'Translation', max_length=1000, help_text='Modern Greek translation')

    def get_absolute_url(self):
        return reverse('bible:verse-detail', kwargs={
            'chapter_id': self.chapter,
            'verse_id': self.pk
        })

    def __unicode__(self):
        return self.number + ' - ' + Truncator(self.original_text).chars(50)


class Annotation(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.PROTECT)
    number = models.CharField(
        max_length=5, help_text='Annotation number of the verse\'s word')
    phrase = models.CharField(
        max_length=60, help_text='The words that are annotated')
    # TextField.max_length only for the form, not the db field
    annotation = models.TextField(max_length=5000)

    def __unicode__(self):
        return self.phrase

    def get_absolute_url(self):
        return reverse('bible:annotation-detail', kwargs={
            'verse_id': self.verse,
            'annotation_id': self.pk
        })

# BOOKMARKS many to many


class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name="User")


class BookmarkBook(BookmarkBase):

    class Meta:
        db_table = "bookmark_book"

    obj = models.ForeignKey(Book, verbose_name="Book")
