# all the classes there (but not copy) is about documents, not about library system. Copy connects library and documents
from django.db import models
from library.models import UserCard, Library
from users.models import Author, Patron


class Keyword(models.Model):
    word = models.CharField(max_length=255)


# there are 3 types of documents: books, journal articles and audio/video files
class Document(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='documents')
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, related_name='documents')
    price_value = models.IntegerField()
    #image = models.ImageField(blank=True)
    keywords = models.ManyToManyField(Keyword, related_name='documents')  # i do not know


class Editor(models.Model):
    first_name = models.CharField(max_length=250)
    second_name = models.CharField(max_length=250)


class Journal(models.Model):
    title = models.CharField(max_length=250)


class Issue(models.Model):
    publication_date = models.DateField()
    editors = models.ManyToManyField(Editor, related_name='issues')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='issues')


class JournalArticles(Document):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='journal_articles')


class Book(Document):
    is_best_seller = models.BooleanField()
    edition = models.IntegerField()
    publisher = models.CharField(max_length=100)
    publish_time = models.DateField()


class ReferenceBook (Book):
    pass

class AudioVideo(Document):
    pass


class Copy(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, related_name='copies')
    user_card = models.ForeignKey(UserCard, on_delete=models.DO_NOTHING, related_name='copies')
    number = models.IntegerField()
    is_checked_out = models.BooleanField()
    booking_date = models.DateField()