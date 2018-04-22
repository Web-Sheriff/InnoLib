import datetime
import re

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now

'''
Class that generates LMS 
'''

# RENEW


class Library(models.Model):
    mail = models.EmailField(default='InnoLib@yandex.ru', max_length=64)
    password = models.CharField(default='InnoTest', max_length=32)

    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.all())


''' 
every user has exactly one user card
user card contains all copies, which user checked out
user card has unique number
'''

'''
Login class for identifying in the system
'''

class Login(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


# All the classes below (but not copy) are about documents. Copy connects library and documents

'''
Class of books authors
'''


class Author(models.Model):
    name = models.CharField(max_length=64)


'''
Class for searching in the system with keywords of CharField types
'''


class Keyword(models.Model):
    word = models.CharField(max_length=256)


# There are 3 types of documents: books, journal articles and audio/video files
'''
Class describing types of models kept in the library & all operations to apply with them
'''


class Document(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='documents')
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField(Author, related_name='documents')
    price_value = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='documents')

    studentsQueue = models.ManyToManyField("Student", related_name='documents')
    instructorsQueue = models.ManyToManyField("Instructor", related_name='documents')
    TAsQueue = models.ManyToManyField("TA", related_name='documents')
    visitingProfessorsQueue = models.ManyToManyField("VisitingProfessor", related_name='documents')
    professorsQueue = models.ManyToManyField("Professor", related_name='documents')

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)

    def queue_type(self, doc, user):
        if isinstance(user, Student):
            return doc.studentsQueue
        elif isinstance(user, Instructor):
            return doc.instructorsQueue
        elif isinstance(user, TA):
            return doc.TAsQueue
        elif isinstance(user, VisitingProfessor):
            return doc.visitingProfessorsQueue
        else:
            return doc.professorsQueue

    def first_in_queue(self, doc):
        if doc.studentsQueue.count() > 0:
            return doc.studentsQueue.first()
        elif doc.instructorsQueue.count() > 0:
            return doc.instructorsQueue.first()
        elif doc.TAsQueue.count() > 0:
            return doc.TAsQueue.first()
        elif doc.visitingProfessorsQueue.count() > 0:
            return doc.visitingProfessorsQueue.first()
        elif doc.professorsQueue.count() > 0:
            return doc.professorsQueue.first()
        else:
            return False

    def has_queue(self):
        if self.studentsQueue.count() + self.instructorsQueue.count() + self.TAsQueue.count() + self.professorsQueue.count() + self.visitingProfessorsQueue.count() > 0:
            return False
        else:
            return True


''' Derivative from Document class with only book features'''


# Document

class Book(Document):
    is_best_seller = models.BooleanField(default=False)
    edition = models.CharField(max_length=128)
    publisher = models.CharField(max_length=64)
    year = models.IntegerField()
    #authors_names = models.

    def booking_period(self, user):
        if isinstance(user, Faculty):
            return datetime.timedelta(days=28)
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(days=7)
        if self.is_best_seller:
            return datetime.timedelta(days=14)
        return datetime.timedelta(days=21)


''' Derivative from Document class with only book features'''


class ReferenceBook(Book):
    authors = models.ManyToManyField(Author, related_name='reference')
    keywords = models.ManyToManyField(Keyword, related_name='reference')


''' Derivative from Document class with only audio and video features'''


class AudioVideo(Document):
    publisher = models.CharField(max_length=64)
    year = models.IntegerField()

    def booking_period(self, user):
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(weeks=1)
        return datetime.timedelta(weeks=2)


''' Specific class for editing information in text sources by Editors (updaters of sources)'''


class Editor(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)


''' Specaial class for Journals (not Document successor) because of special booking case'''


class Journal(models.Model):
    title = models.CharField(max_length=128)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='journals')
    authors = models.ManyToManyField(Author, related_name='journals')
    price_value = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='journals')

    def booking_period(self, user):
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(weeks=1)
        return datetime.timedelta(weeks=2)


''' Issye information which all journals are going to have'''


class Issue(models.Model):
    publication_date = models.DateField()
    editors = models.ManyToManyField(Editor, related_name='issues')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='issues')


'''Journal aricles differing from other sources to book'''


class JournalArticles(Document):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='journal_articles')


''' The main class about copies of documents using in UserCard'''


class Copy(models.Model):
    user_card = models.ForeignKey('UserCard', default=None, on_delete=models.DO_NOTHING, related_name='copies', null=True)
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, related_name='copies')
    number = models.IntegerField()
    is_checked_out = models.BooleanField(default=False)
    need_to_return = models.BooleanField(default=False)
    booking_date = models.DateField(null=True)
    overdue_date = models.DateField(null=True)
    renew = models.ForeignKey("Librarian", on_delete=models.DO_NOTHING, related_name='renew', null=True)
    weeks_renew = models.ForeignKey("Librarian", on_delete=models.DO_NOTHING, related_name='weeks_renew', null=True)

    # def check_out(self, user):
    #     if isinstance(self.document, ReferenceBook):
    #         return False
    #     if not self.document.copies.filter(user=user).exists():
    #         return False
    #     self.is_checked_out = True
    #     self.user = user
    #     self.booking_date = datetime.date.today()
    #     self.overdue_date = self.booking_date + self.document.booking_period(user)
    #     self.save()
    #     return True

    def is_overdue(self):
        return now() > self.overdue_date

    def overdue(self):
        return now() - self.overdue_date


# All the classes below are about users

''' The main predecessor of all Patron class derivatives with unique information from login to address'''


# there are 2 types of users: patrons and librarians
class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    mail = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    fine = models.IntegerField(default=0, null=True)


''' UserCard class as contact information which librarian deals with'''


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_card')
    library = models.ForeignKey(Library, default=None, on_delete=models.DO_NOTHING, related_name='user_cards')
    library_card_number = models.IntegerField(default=None)


''' Special subclass for documents that can be accessible'''


# class AvailableDocs(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='available_documents')
#     document = models.OneToOneField(Document, on_delete=models.DO_NOTHING)
#     rights_date = models.DateField(now(), null=True, blank=True)
#
#     def check_date(self):
#         if self.rights_date != datetime.date.today():
#             queue = self.document.queue_type(doc=self.document, user=self.user)
#             queue.exclude(user_card=self.user.user_card)
#             queue.model.save()
#             self.user.available_documents.exclude(document=self.document, user=self.user)
#             self.user.available_documents.model.save()
#             if not self.document.has_queue():
#                 return False
#             first = Document.first_in_queue(doc=self.document)
#             first.available_documents.create(document=self.document, user=first)
#             Librarian.notify(user=first, document=self.document)


# there are 3 types of patrons: students, faculties and visiting professors
'''The main successor of User with clue features for it'''


class Patron(User):

    # renew the document for n weeks
    def renew(self, queue=Copy.renew):
        # queue.add(self)
        # queue.model.save()
        pass

    # search for the documents using string
    def search_doc(self, string):
        d1 = self.search_doc_author(string)
        d2 = self.search_doc_title(string)
        d3 = self.search_doc_keywords(string)
        d4 = d1 | d2 | d3
        return d4.distinct()

    # search for the documents using string, which is the name of the author
    def search_doc_author(self, name):
        documents = self.user_card.library.documents.filter(authors__name__contains=name).distinct()
        return documents

    # search for the documents using string, which is the title
    def search_doc_title(self, name):
        documents = self.user_card.library.documents.filter(title__contains=name).distinct()
        return documents

    # search for the documents using string, which contains keywords
    def search_doc_keywords(self, string):
        words = re.split('[ ,.+;:]+', string)
        documents = self.user_card.library.documents.filter(keywords__word__in=words).distinct()
        return documents

    # check out some copy of the document. If it is not possible returns False
    def check_out_doc(self, document):
        for copy in self.user_card.copies.all():
            if copy.document == document:
                return False  # user has already checked this document
        queue = document.queue_type(doc=document, user=self)
        queue.add(self)
        queue.model.save()
        return True  # user got into queue

    # we cannot return_doc feature because user cannot return it by himself. this action should do the librarian
    # return copy of the document to the library. If it is not possible returns False
    # def return_doc(self, document):
    #     for copy in self.user_card.copies.all():
    #         if copy.document == document:
    #             HandOverRequest.objects.create(user_card=self.user_card, copy=copy)
    #             self.user_card.copies.exclude(copy)
    #             self.user_card.save()
    #             # Librarian.handed_over_copies.add(copy)
    #             return True
    #     return False  # no such document

    def has_overdue(self):  # bool
        for copy in self.user_card.copies.objects.all():
            if copy.overdue_date > datetime.date:
                return True
        return False

    def type(self):
        if isinstance(self, Student):
            return "Student"
        if isinstance(self, Instructor):
            return "Instructor"
        if isinstance(self, TA):
            return "TA"
        if isinstance(self, Professor):
            return "Professor"
        if isinstance(self, VisitingProfessor):
            return "Visiting Professor"


''' Student patron'''


class Student(Patron):
    pass


''' Faculty parton'''


class Faculty(Patron):
    pass


''' Visiting professor patron'''


class VisitingProfessor(Patron):
    pass


''' Instructor patron'''


class Instructor(Faculty):
    pass


'''TA patron'''


class TA(Faculty):
    pass


'''Professor patron'''


class Professor(Faculty):
    pass


''' The main moderator user - Librarian'''


class Librarian(User):

    level_of_privileges = models.IntegerField(default=1)

    def handle_book(self, user, doc):
        queue = doc.document.queue_type(doc=doc, user=user)
        if user.id == queue.first().id:
            for copy in doc.copies:
                if not copy.is_checked_out:
                    copy.is_checked_out = True
                    user.user_card.copies.add(copy)
                    copy.booking_date = datetime.date.today()
                    queue.exclude(user_card=user.user_card)
                    queue.model.save()
                    user.user_card.save()
                    user.save()
                    copy.save()
                    return True
            print("This book have not any copy")
            return False
        else:
            print("This user is not first in queue")
            return False

    def send_email(self, to, subject, message):
        library = Library.objects.first()
        send_mail(auth_user=library.mail, auth_password=library.password, from_email=library.mail,
                  subject=subject, message=message, recipient_list=to)

    def renew_request(self):
        for renew in Copy.objects.all():
            weeks = renew.weeks_renew
            delta = datetime.timedelta(days=weeks // 7)
            renew.overdue_date += delta

    def outstanding_request(self, doc):
        if self.level_of_privileges >= 2:
            self.remove_all_copies_without_check(doc)

            message = 'Dear user, sorry but you have been removed from the queue on document "' + doc.title + '" due to outstanding request'
            removed_users_mails = []
            for user in doc.studentsQueue:
                removed_users_mails.append(user.mail)
            for user in doc.instructorsQueue:
                removed_users_mails.append(user.mail)
            for user in doc.TAsQueue:
                removed_users_mails.append(user.mail)
            for user in doc.professorsQueue:
                removed_users_mails.append(user.mail)
            for user in doc.visitingProfessorsQueue:
                removed_users_mails.append(user.mail)
            send_mail(message=message, subject='Outstanding request', from_email=Library.mail, recipient_list=removed_users_mails, auth_user=Library.mail, auth_password=Library.password)

            message = 'Dear user, please return the copy of "' + doc.title + '" immediately due to outstanding request. You have only 1 day to return this document'
            users_with_copy = []
            for copy in doc.copies:
                if copy.is_checked_out:
                    users_with_copy.append(copy.user_card.user.mail)
                    copy.overdue_date = datetime.date.today() + datetime.timedelta(days=1)
            send_mail(message=message, subject='Outstanding request', from_email=Library.mail, recipient_list=users_with_copy, auth_user=Library.mail, auth_password=Library.password)
        else:
            print("You cannot perform this action")
        # Допили этот метод

    def notify(self, user, document):
        user.available_documents.create(document=document, user=user)
        send_mail(
            message='Dear user, you have 1 day to take a copy of document you queued up for. After the expiration of this period you will lose this opportunity and will be removed from the queue. Good luck. Your InnoLib',
            subject='Waiting notification', from_email=Library.mail, recipient_list=user.mail, auth_user=Library.mail, auth_password=Library.password)
        print("The message with notifying was sent to the email of "+user.first_name+" "+user.second_name+" about "+document.title)

    def accept_doc(self, user, copy):
        copy.is_checked_out = False
        user.user_card.copies.exclude(copy)
        user.user_card.save()
        copy.save()

        first = Document.first_in_queue(doc=copy.document)
        self.notify(first, copy.document)

    def accept_doc_after_outstanding_request(self, user, copy):
        user.user_card.copies.exclude(copy)
        user.user_card.save()
        copy.delete()
        copy.save()

    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.objects.all())

    def see_waiting_list(self, doc):
        queue = []
        for i in doc.studentsQueue.all():
            queue.append(i)
        for i in doc.instructorsQueue.all():
            queue.append(i)
        for i in doc.TAsQueue.all():
            queue.append(i)
        for i in doc.professorsQueue.all():
            queue.append(i)
        for i in doc.visitingProfessorsQueue.all():
            queue.append(i)
        print("queue for this book:")
        for i in queue:
            print(i.first_name + i.second_name + i.type())

    def patrons_docs(self, user, doc):
        for copy in user.user_card.copies.all():
            if copy.document == doc:
                print(user.first_name + " " + user.second_name + ": " + doc.title + ": " + copy.number)

    def unchecked_copies(self, doc):
        print("there are " + str(self.user_card.library.count_unchecked_copies(
            doc)) + "unchecked copies of document " + doc.title + "in library.")

    def check_overdue_copies(self):
        for card in UserCard.objects.all():
            for copy in card.copies:
                if copy.if_overdue():
                    card.user.fine += copy.overdue * copy.document.price_value

    def create_copies(self, document, number):
        if self.level_of_privileges >= 2:
            for i in range(number):
                copy = Copy.objects.create(document=document, number=number)
                copy.save()
        else:
            print("You cannot perform this action")

    def create_av(self, library, title, publisher, year, price_value):
        if self.level_of_privileges >= 2:
            av = AudioVideo.objects.create(library=library, title=title, price_value=price_value, publisher=publisher, year=year)
            av.save()
            return av
        else:
            print("You cannot perform this action")

    def create_user(self, class_model, first_name, second_name, login, password, address, phone_number, mail):
        if self.level_of_privileges >= 2:
            library_card_number = User.objects.last().user_card.library_card_number + 1
            user = class_model.objects.create(login=login,
                                              password=password, first_name=first_name,
                                              second_name=second_name, address=address,
                                              phone_number=phone_number, mail=mail)
            user_card = UserCard.objects.create(user=user, library_card_number=library_card_number, library=self.user_card.library)
            user.save()
            user_card.save()
            return user
        else:
            print("You cannot perform this action")

    def remove_object(self, class_model, obj):
        if self.level_of_privileges == 3:
            class_model.objects.get(id=obj.id).delete()
            obj.save()
        else:
            print("You cannot perform this action")

    def remove_copies(self, document, count):
        if self.level_of_privileges == 3:
            for copy in document.copies:
                if not copy.is_checked_out:
                    copy.delete()
                    copy.save()
                    count -= 1
                    if count == 0:
                        break
            document.copies.save()
            document.save()
        else:
            print("You cannot perform this action")

    def create_authors(self, list_of_names):
        if self.level_of_privileges >= 2:
            list = []
            for name in list_of_names:
                author = Author.objects.create(name=name)
                author.save()
                list.append(author)
            return list

    def create_author(self, name):
        if self.level_of_privileges >= 2:
            author = Author.objects.create(name=name)
            author.save()

    def create_book(self, library, is_best_seller, reference, title, price_value, edition, publisher, year,
                    authors_names):
        if self.level_of_privileges >= 2:
            authors = self.create_authors(authors_names)
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            for author in authors:
                model.authors.add(author)
            model.save()
            return model
        else:
            print("You cannot perform this action")

    def remove_all_copies(self, document):
        if self.level_of_privileges == 3:
            for copy in document.copies:
                if not copy.is_checked_out:
                    copy.delete()
                    copy.save()
            document.copies.save()
            document.save()
        else:
            print("You cannot perform this action")

    def remove_all_copies_without_check(self, document):
        for copy in document.copies:
            if not copy.is_checked_out:
                copy.delete()
                copy.save()
        document.copies.save()
        document.save()

    # def patron_information(self, id):
    #     try:
    #         patron = Patron.objects.get(id=id)
    #     except ObjectDoesNotExist:
    #         print("p", id, ": information no available, patron does not exist.", sep='')
    #         return
    #     print("p", id, sep='')
    #     print(" Name:", patron.first_name, patron.second_name)
    #     print(" Address:", patron.address)
    #     print(" Phone Number:", patron.phone_number)
    #     print(" Lib. card ID:", patron.user_card.id)
    #
    #     if isinstance(patron, Faculty):
    #         print(" Type: Faculty")
    #     else:
    #         print(" Type: Student")
    #
    #     print(" (document checked-out, due date): ")
    #     print("[", end='')
    #
    #     copies = patron.user_card.copies
    #     for copy in copies.all():
    #         if isinstance(copy.document, AudioVideo):
    #             print("(av", copy.document.id, ',', copy.overdue_date, ')', sep='', end='')
    #         else:
    #             print("(b", copy.document.id, ',', copy.overdue_date, ')', sep='', end='')
    #             if copy != copies.last():
    #                 print(", ", end='')
    #     print("]")


class Admin(User):

    def add_librarian(self, first_name, second_name, login, password, address, phone_number, mail, level_of_privileges):
        library_card_number = User.objects.last().user_card.library_card_number + 1
        librarian = Librarian.objects.create(first_name=first_name, second_name=second_name, login=login, password=password,
                                             address=address, phone_number=phone_number, mail=mail, level_of_privileges=level_of_privileges)
        UserCard.objects.create(user=librarian, library=self.user_card.library,
                                library_card_number=library_card_number)
        return librarian

    def change_level_of_privileges(self, librarian, level_of_privileges):
        librarian.level_of_privileges = level_of_privileges

    def delete_librarian(self, librarian):
        Librarian.objects.get(id=librarian.id).delete()
        librarian.save()
