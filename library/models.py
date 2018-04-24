import datetime
import logging

from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now

'''
Class that generates LMS 
'''


class Logger:
    logging.basicConfig(filename='InnoLib.log', level=logging.INFO, format=u'[%(asctime)s] in /%(filename)s (line:%(lineno)d) #%(levelname)s : %(message)s')
    logging.info("Innopolis Library working")


class Library(models.Model):
    mail = models.EmailField(default='InnoLib@yandex.ru', max_length=64)
    password = models.CharField(default='InnoTest', max_length=32)

    def is_admin_exists(self):
        if Admin.objects.first() is None:
            return False
        return True

    def create_admin(self):
        logging.info("Library trying to create an admin")
        if not self.is_admin_exists():
            admin = Admin.objects.create(login='admin', password='adminadmin', mail='test@yandex.ru',
                                         first_name='Vyacheslav', second_name='Vasilev', address='Innopolis',
                                         phone_number='88005553535')
            user_card = UserCard.objects.create(user=admin, library=self, library_card_number=0)
            self.is_admin_exists = True
            user_card.save()
            admin.save()
            self.save()
            logging.info("Library created an admin")
            return Admin
        logging.info("Library tried to create an admin, but admin already exists")
        return False

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

    studentsQueue = models.ManyToManyField("Student", related_name='documents', blank=True)
    instructorsQueue = models.ManyToManyField("Instructor", related_name='documents', blank=True)
    TAsQueue = models.ManyToManyField("TA", related_name='documents', blank=True)
    visitingProfessorsQueue = models.ManyToManyField("VisitingProfessor", related_name='documents', blank=True)
    professorsQueue = models.ManyToManyField("Professor", related_name='documents', blank=True)

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)

    def queue_type(self, user):
        if isinstance(user, Student):
            return self.studentsQueue
        elif isinstance(user, Instructor):
            return self.instructorsQueue
        elif isinstance(user, TA):
            return self.TAsQueue
        elif isinstance(user, VisitingProfessor):
            return self.visitingProfessorsQueue
        else:
            return self.professorsQueue

    def first_in_queue(self):
        if self.studentsQueue.count() > 0:
            return self.studentsQueue.first()
        elif self.instructorsQueue.count() > 0:
            return self.instructorsQueue.first()
        elif self.TAsQueue.count() > 0:
            return self.TAsQueue.first()
        elif self.visitingProfessorsQueue.count() > 0:
            return self.visitingProfessorsQueue.first()
        elif self.professorsQueue.count() > 0:
            return self.professorsQueue.first()
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
    fine = models.IntegerField(default=0, blank=True)
    status = models.CharField(default='User', max_length=32)

    ''' UserCard class as contact information which librarian deals with'''


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_card')
    library = models.ForeignKey(Library, default=None, on_delete=models.DO_NOTHING, related_name='user_cards')
    library_card_number = models.IntegerField(default=None)


# there are 3 types of patrons: students, faculties and visiting professors
'''The main successor of User with clue features for it'''


class Patron(User):

    # renew the document for n weeks
    def renew(self, queue=Copy.renew):
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to renew the copy of document")
        # queue.add(self)
        # queue.model.save()
        logging.info("Patron " + self.first_name + " " + self.second_name + " renewed the copy of document")

    def search_by_availability(self):  # this search returns all documents which have at least one available copy.
        logging.info("Patron " + self.first_name + self.second_name + " trying to search documents by availability")
        documents = Document.objects.all().filter(copies__is_checked_out=False)
        list_of_ids = [documents.first().id]
        docs = documents[1:]
        i = 0
        for doc in docs:
            if doc.id != list_of_ids[i]:
                list_of_ids.append(doc.id)
                i += 1
        res = Document.objects.all().filter(id__in=list_of_ids)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents by availability ")
        return res

    def search_by_title(self, title):  # this search returns all documents which titles contains 'title'.
        # For example, if document have title 'Test', search by 'te' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by title " + title)
        res = Document.objects.all().filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents by title " + title)
        return res

    def search_by_author(self, author):  # this search returns all documents which authors names contains 'author'.
        # For example, if document have authors 'Tolkien' and 'Rowling', search by 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by author " + author)
        res = Document.objects.all().filter(authors__name__icontains=author)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents by author " + author)
        return res

    def search_by_title_available(self, title):  # this search returns all available documents which titles contains 'title'.
        # For example, if document have title 'Test' and at least one available copy, search by 'te' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by title " + title)
        res = self.search_by_availability().filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found available documents by title " + title)
        return res

    def search_by_author_available(self, author):  # this search returns all available documents which authors names contains 'author'.
        # For example, if document have authors 'Tolkien' and 'Rowling' and at least one available copy, search by 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by author " + author)
        res = self.search_by_availability().filter(authors__name__icontains=author)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found available documents by author " + author)
        return res

    def search_by_author_and_title(self, title, author):  # this search returns all documents which authors names contains 'author' and titles contains 'title'.
        # For example, if document have title 'Test' and authors 'Tolkien' and 'Rowling', search by 'te', 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by author " + author + " and title " + title)
        res = Document.objects.all().filter(authors__name__icontains=author).filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents by author " + author + " and title " + title)
        return res

    def search_by_author_and_title_available(self, author, title):  # this search returns all available documents which authors names contains 'author' and titles contains 'title'.
        # For example, if document have title 'Test' and authors 'Tolkien' and 'Rowling' and at least one available copy, search by 'te', 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by author " + author + " and title " + title)
        res = self.search_by_availability().filter(authors__name__icontains=author).filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found available documents by author " + author + " and title " + title)
        return res

    # patron cannot check out some copy of the document by himself, so he is just trying to got in queue. If it is not possible returns False
    def check_out_doc(self, document):
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to got in queue for the document " + document.title)
        for copy in self.user_card.copies.all():
            if copy.document.id == document.id:
                # print("You cannot got in queue for this document because you're already have a copy of this document")
                logging.info("Patron " + self.first_name + " " + self.second_name + " cannot got in queue because he is already have a copy of this document")
                return False  # user has already checked this document
        queue = document.queue_type(user=self)
        for user in queue.all():
            if user.id == self.id:
                # print("You cannot got in queue for this document because you're already in this queue")
                logging.info("Patron " + self.first_name + " " + self.second_name + " cannot got in queue because he is already in this queue")
                return False
        queue.add(self)
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
        # logging.info("Patron " + self.first_name + self.second_name + " trying to check if he has any overdue")
        for copy in self.user_card.copies.objects.all():
            if copy.overdue_date > datetime.date:
                # logging.info("Patron " + self.first_name + self.second_name + " found that he has overdue for copy of document " + copy.document.title)
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to handle a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name)
        queue = doc.queue_type(user=user)
        if queue.all().count() > 0:
            if user.id == queue.first().id:
                for copy in doc.copies.all():
                    if not copy.is_checked_out:
                        copy.is_checked_out = True
                        user.user_card.copies.add(copy)
                        copy.booking_date = datetime.date.today()
                        queue.remove(user)
                        doc.save()
                        user.user_card.save()
                        user.save()
                        copy.save()
                        logging.info("Librarian " + self.first_name + " " + self.second_name + " handled a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name)
                        return True
                # print("This book have not any available copy")
                logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to handle a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name + ", but this document have not any available copy")
                return False
            else:
                logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to handle a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name + ", but this patron not first in queue")
                # print("This user is not first in queue")
                return False
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to handle a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name + ", but this patron not first in queue")
            # print("This user is not first in queue")
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an outstanding request for the document " + doc.title)
        if self.level_of_privileges >= 2:
            self.remove_all_copies_without_check(doc)

            message = 'Dear user, sorry but you have been removed from the queue on document "' + doc.title + '" due to an outstanding request'
            removed_users_mails = []
            for user in doc.studentsQueue.all():
                removed_users_mails.append(user.mail)
            for user in doc.instructorsQueue.all():
                removed_users_mails.append(user.mail)
            for user in doc.TAsQueue.all():
                removed_users_mails.append(user.mail)
            for user in doc.professorsQueue.all():
                removed_users_mails.append(user.mail)
            for user in doc.visitingProfessorsQueue.all():
                removed_users_mails.append(user.mail)
            if len(removed_users_mails) > 0:
                send_mail(message=message, subject='Outstanding request', from_email=Library.mail, recipient_list=removed_users_mails, auth_user=Library.mail, auth_password=Library.password)
                logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patrons who was removed from deleted queue for the document " + doc.title + " due to an outstanding request")

            message = 'Dear user, please return the copy of "' + doc.title + '" immediately due to an outstanding request. You have only 1 day to return this document'
            users_with_copy = []
            for copy in doc.copies.all():  # we are do not checking copy for is_checked_out because all checked out copies already deleted
                users_with_copy.append(copy.user_card.user.mail)
                copy.overdue_date = datetime.date.today() + datetime.timedelta(days=1)
                copy.save()
            if len(users_with_copy):
                send_mail(message=message, subject='Outstanding request', from_email=Library.mail, recipient_list=users_with_copy, auth_user=Library.mail, auth_password=Library.password)
                logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patrons who should to immediately return the document " + doc.title + " due to an outstanding request")
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an outstanding request for the document " + doc.title + ", but he have not enough level of privileges")
            # print("You cannot perform this action")

    def notify(self, user, document):
        message='Dear user, you have 1 day to take a copy of ' + document.title + ' you queued up for. After the expiration of this period you will lose this opportunity and will be removed from the queue. Good luck. Your InnoLib'
        send_mail(
            message='Dear user, you have 1 day to take a copy of document you queued up for. After the expiration of this period you will lose this opportunity and will be removed from the queue. Good luck. Your InnoLib',
            subject='Waiting notification', from_email=Library.mail, recipient_list=user.mail, auth_user=Library.mail, auth_password=Library.password)
        logging.info("The message with notifying was sent to the email " + user.mail + " of " + user.first_name + " " + user.second_name)

    def accept_doc(self, user, doc):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to accept the copy of document " + doc.title + " from patron " + user.first_name + " " + user.second_name)
        for copy in doc.copies.all():
            if copy.is_checked_out:
                if copy.user_card.id == user.user_card.id:
                    copy.is_checked_out = False
                    copy.user_card = None
                    user.user_card.copies.all().exclude(id=copy.id)
                    user.save()
                    user.user_card.save()
                    copy.save()
                    copy.booking_date = None
                    copy.save()
                    logging.info("Librarian " + self.first_name + " " + self.second_name + " accepted the copy of document " + doc.title + " from patron " + user.first_name + " " + user.second_name)
                    # first = copy.document.first_in_queue()
                    # self.notify(first, copy.document)
                    # logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patron " + user.first_name + " " + user.second_name + " that now he is first in queue for the document " + doc.title)
                    return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to accept the copy of document " + doc.title + " from patron " + user.first_name + " " + user.second_name + ", but he have not any copy of this document")
        # print("This user have not any copy of this document")
        return False

    def accept_doc_after_outstanding_request(self, user, copy):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to accept the copy of document " + copy.document.title + " from patron " + user.first_name + " " + user.second_name + " after outstanding request")
        user.user_card.copies.remove(copy)
        user.user_card.save()
        user.save()
        copy.delete()
        logging.info("Librarian " + self.first_name + " " + self.second_name + " accepted the copy of document " + copy.document.title + " from patron " + user.first_name + " " + user.second_name + " after outstanding request")

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

    def create_keywords(self, list_of_keywords):
        if self.level_of_privileges >= 2:
            list = []
            for word in list_of_keywords:
                keyword = Keyword.objects.create(word=word)
                keyword.save()
                list.append(keyword)
            return list

    def create_authors(self, list_of_names):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an authors " + list_of_names)
        if self.level_of_privileges >= 2:
            list = []
            for name in list_of_names:
                author = Author.objects.create(name=name)
                author.save()
                list.append(author)
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created an authors " + list_of_names)
            return list
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an authors " + list_of_names + ", but he have not enough level of privileges")

    def create_author(self, name):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an author " + name)
        if self.level_of_privileges >= 2:
            author = Author.objects.create(name=name)
            author.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created an author " + name)
            return author
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an author " + name + ", but he have not enough level of privileges")

    def create_book(self, library, is_best_seller, reference, title, price_value, edition, publisher, year):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create a book " + title)
        if self.level_of_privileges >= 2:
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created a book " + title)
            return model
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_book_new(self, library, is_best_seller, reference, title, price_value, edition, publisher, year, authors, keywords):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create a book " + title)
        if self.level_of_privileges >= 2:
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            for author in authors:
                model.authors.add(author)
            model.save()
            for keyword in keywords:
                model.keywords.add(keyword)
            model.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created a book " + title)
            return model
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_book_with_authors_names(self, library, is_best_seller, reference, title, price_value, edition, publisher, year, authors, keywords):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create a book " + title)
        if self.level_of_privileges >= 2:
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            auth = self.create_authors(authors)
            for author in auth:
                model.authors.add(author)
            model.save()
            key = self.create_keywords(keywords)
            for keyword in key:
                model.keywords.add(keyword)
            model.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created a book " + title)
            return model
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_copies(self, document, number):
        if document is None:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create copies of uncreated document")
            return False
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create " + str(number) + " copies of document " + document.title)
        if self.level_of_privileges >= 2:
            for i in range(number):
                copy = Copy.objects.create(document=document, number=number)
                copy.save()
                logging.info("Librarian " + self.first_name + " " + self.second_name + " created " + str(number) + " copies of document " + document.title)
                return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create " + str(number) + " copies of document " + document.title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_av(self, library, title, publisher, year, price_value):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create AV " + title)
        if self.level_of_privileges >= 2:
            av = AudioVideo.objects.create(library=library, title=title, price_value=price_value, publisher=publisher, year=year)
            av.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created AV " + title)
            return av
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create AV " + title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_user(self, class_model, first_name, second_name, login, password, address, phone_number, mail):
        if class_model is Student:
            status = 'Student'
        elif class_model is Instructor:
            status = 'Instructor'
        elif class_model is TA:
            status = 'TA'
        elif class_model is Professor:
            status = 'Professor'
        elif class_model is VisitingProfessor:
            status = 'Visiting Professor'
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create user " + first_name + " " + second_name + ", but he cannot create user of this type")
            return False

        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create user " + first_name + " " + second_name)
        if self.level_of_privileges >= 2:
            library_card_number = User.objects.last().user_card.library_card_number + 1
            user = class_model.objects.create(login=login,
                                              password=password, first_name=first_name,
                                              second_name=second_name, address=address,
                                              phone_number=phone_number, mail=mail, status=status)
            user_card = UserCard.objects.create(user=user, library_card_number=library_card_number, library=self.user_card.library)
            user.save()
            user_card.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created user " + first_name + " " + second_name)
            return user
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create user " + first_name + " " + second_name + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def create_user_with_library_card_number(self, class_model, first_name, second_name, login, password, address, phone_number, mail, library_card_number):
        if class_model is Student:
            status = 'Student'
        elif class_model is Instructor:
            status = 'Instructor'
        elif class_model is TA:
            status = 'TA'
        elif class_model is Professor:
            status = 'Professor'
        elif class_model is VisitingProfessor:
            status = 'Visiting Professor'
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create user " + first_name + " " + second_name + ", but he cannot create user of this type")
            return False

        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create " + status + " " + first_name + " " + second_name)
        if self.level_of_privileges >= 2:
            user = class_model.objects.create(login=login,
                                              password=password, first_name=first_name,
                                              second_name=second_name, address=address,
                                              phone_number=phone_number, mail=mail, status=status)
            user_card = UserCard.objects.create(user=user, library_card_number=library_card_number, library=self.user_card.library)
            user.save()
            user_card.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created " + status + " " + first_name + " " + second_name)
            return user
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create " + status + " " + first_name + " " + second_name + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def remove_object(self, obj):
        if isinstance(obj, User):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove user " + obj.first_name + " " + obj.second_name)
        elif isinstance(obj, Document):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove document " + obj.title)
        elif isinstance(obj, Admin):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove admin " + obj.first_name + " " + obj.second_name)
            return False

        if self.level_of_privileges == 3:
            obj.delete()

            if isinstance(obj, User):
                logging.info("Librarian " + self.first_name + " " + self.second_name + " removed user " + obj.first_name + " " + obj.second_name)
            elif isinstance(obj, Document):
                logging.info("Librarian " + self.first_name + " " + self.second_name + " removed document " + obj.title)
            return True

        if isinstance(obj, User):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove user " + obj.first_name + " " + obj.second_name + ", but he have not enough level of privileges")
        elif isinstance(obj, Document):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove document " + obj.title + ", but he have not enough level of privileges")

    def remove_copies(self, document, count):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove " + str(count) + " copies of document" + document.title)
        if self.level_of_privileges == 3:
            for copy in document.copies:
                if not copy.is_checked_out:
                    copy.delete()
                    count -= 1
                    if count == 0:
                        break
            document.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " removed " + str(count) + " copies of document" + document.title)
            return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove " + str(count) + " copies of document" + document.title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def remove_all_copies(self, document):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove all copies of document" + document.title)
        if self.level_of_privileges == 3:
            for copy in document.copies:
                if not copy.is_checked_out:
                    copy.delete()
            document.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " removed all copies of document" + document.title)
            return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove all copies of document" + document.title + ", but he have not enough level of privileges")
        # print("You cannot perform this action")

    def remove_all_copies_without_check(self, document):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove all copies of document" + document.title + " without check")
        for copy in document.copies.all():
            if not copy.is_checked_out:
                copy.delete()
        document.save()
        logging.info("Librarian " + self.first_name + " " + self.second_name + " removed all copies of document" + document.title + " without check")

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
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to add librarian" + first_name + " " + second_name)
        library_card_number = User.objects.last().user_card.library_card_number + 1
        librarian = Librarian.objects.create(first_name=first_name, second_name=second_name, login=login, password=password,
                                             address=address, phone_number=phone_number, mail=mail, level_of_privileges=level_of_privileges)
        user_card = UserCard.objects.create(user=librarian, library=self.user_card.library, library_card_number=library_card_number)
        librarian.save()
        user_card.save()
        logging.info("Admin " + self.first_name + " " + self.second_name + " added librarian" + first_name + " " + second_name)
        return librarian

    def change_level_of_privileges(self, librarian, level_of_privileges):
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to change level of privileges of librarian" + librarian.first_name + " " + librarian.second_name)
        librarian.level_of_privileges = level_of_privileges
        logging.info("Admin " + self.first_name + " " + self.second_name + " changed level of privileges of librarian" + librarian.first_name + " " + librarian.second_name)

    def delete_librarian(self, librarian):
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to delete librarian" + librarian.first_name + " " + librarian.second_name)
        librarian.delete()
        logging.info("Admin " + self.first_name + " " + self.second_name + " deleted librarian" + librarian.first_name + " " + librarian.second_name)
