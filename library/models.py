import datetime
import logging

'''
Now import 'from django.core.mail import send_mail' does not using,
but it will be used when we will uncomment send_mail in send_email feature
(we did it because we do not want to spam in every test)
'''

from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now


'''
Logger is a Class that responsible for logs configurations
'''


class Logger:
    logging.basicConfig(filename='InnoLib.log', level=logging.INFO, format=u'[%(asctime)s] in /%(filename)s (line:%(lineno)d) #%(levelname)s : %(message)s')
    logging.info("Innopolis Library working")


'''
Library is a Class that generates out LMS

Library has next features:
    Create admin (create_admin)
    Check is admin exists in system already (is_admin_exists)
'''


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
                                         phone_number='88005553535', status='Admin')
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
Login is a class for identifying in the system

Login has next two fields:
    Username (username) - char field
    Password (password) - char field
'''


class Login(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


'''
Author is a class of books authors

Authors has only one field:
    Name (name) - char field
'''


class Author(models.Model):
    name = models.CharField(max_length=64)


'''
Keyword is a class of keywords that existing in library and have relations with documents

Keywords has only one field:
    Word (word) - char field
'''


class Keyword(models.Model):
    word = models.CharField(max_length=256)


'''
Document is a class describing types of models kept in the library & all operations to apply with them

Document has five fields that specifying during creation procedure:
    Library (library) - relation with Library
    Title (title) - char field
    Authors (authors) - relation with Author objects that already exists in database
    Price value (price_value) - integer field
    Keywords - relation with Keyword objects that already exists in database
Document has five another fields-relations that represents priority queue for every document
Document has four next features:
    Booking period (booking_period) that determines overdue date during handle book procedure
    And three another features for convenience work with priority queues:
        Queue type (queue_type) that returns the right queue for certain user
        First in queue (first_in_queue) that returns first patron in priority queue for this document
        Has queue (has_queue) that returns boolean value if certain document has any patron in it's queue
'''


class Document(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='documents')
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
        if isinstance(self, Book):
            if isinstance(user, Faculty):
                return datetime.timedelta(days=28)
            if isinstance(user, VisitingProfessor):
                return datetime.timedelta(days=7)
            if self.is_best_seller:
                return datetime.timedelta(days=14)
            return datetime.timedelta(days=21)

        elif isinstance(self, AudioVideo):
            if isinstance(user, VisitingProfessor):
                return datetime.timedelta(days=7)
            return datetime.timedelta(days=14)

        else:
            return datetime.timedelta(days=14)

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


'''
Book is a successor class from Document class with fields that have only Book:

Book has four fields that specifying during creation procedure
    Is best seller (is_best_seller) - boolean field
    Edition (edition) - char field
    Publisher (publisher) - char field
    Year (year) - char field
'''


class Book(Document):
    is_best_seller = models.BooleanField(default=False)
    edition = models.CharField(max_length=128)
    publisher = models.CharField(max_length=64)
    year = models.CharField(max_length=4)


'''
ReferenceBook is a successor class from Book class

ReferenceBook has not any special fields or features, but his type is using in another features
'''


class ReferenceBook(Book):
    pass


'''
AudioVideo is a successor class from Document class with fields that have only AudioVideo

AudioVideo has two fields that specifying during creation procedure:
    Publisher (publisher) - char field
    Year (year) - char field
'''


class AudioVideo(Document):
    publisher = models.CharField(max_length=64)
    year = models.CharField(max_length=4)


'''
Editor is class of Journal editors

Editor has two fields that specifying during creation procedure:
    Name (first_name) - char field
    Surname (second_name) - char field
'''


class Editor(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)


'''
Journal is a class of Journals

Journal has five fields that specifying during creation procedure:
    Title (title) - char field
    Price value (price_value) - integer field
    Library (library) - relation with library
    Authors (authors) - relations with Author objects that already exists in database
    Keywords (keywords) - relation with Keyword objects that already exists in database
Journal has only one next feature:
    Booking period (booking_period) that determines overdue date during handle book procedure
'''


class Journal(models.Model):
    title = models.CharField(max_length=128)
    price_value = models.IntegerField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='journals')
    authors = models.ManyToManyField(Author, related_name='journals')
    keywords = models.ManyToManyField(Keyword, related_name='journals')

    def booking_period(self, user):
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(weeks=1)
        return datetime.timedelta(weeks=2)


'''
Issue is a class of Issues

Issue has three fields that specifying during creation procedure:
    Publication date (publication_date) - date field
    Editors (editors) - relation with Editor objects that already exists in database
    Journal (journal) - relation with Journal
'''


class Issue(models.Model):
    publication_date = models.DateField()
    editors = models.ManyToManyField(Editor, related_name='issues')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='issues')


'''
JournalArticles is a class of Journal Articles

JournalArticles has only one field that specifying during creation procedure:
    Issue (issue) - relation with Issue
'''


class JournalArticles(Document):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='journal_articles')


'''
Copy is a class describing copies of every Document objects:

Copy has eight fields:
    four fields that specifying during creation procedure:
        Document (document) - relation with certain document that never will change, and if document will be deleted, all copies will be deleted by cascade deleting
        Number (number) - integer field. Number of copies existing of certain document
        Booking date (booking_date) - date field of handling a document
        Overdue date (overdue_date) - date field of overdue date that determining by booking_period feature of Document
    three fields that specifying by default by themselves:
        Is checked out (is_checked_out) - boolean field, False by default, becoming True after handling book
        Need to return (need_to_return) - boolean field, False by default, becoming True after overdue_date expiration
        Can renew (can_renew) - boolean field, True by default, becoming False after renew or outstanding request, becoming True after handling book
    and one field that specifying after handling book:
        User card (user_card) - relation with UserCard of certain user that took this copy, Null by default, becoming Null after accepting copy
'''


class Copy(models.Model):
    user_card = models.ForeignKey('UserCard', default=None, on_delete=models.DO_NOTHING, related_name='copies', null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='copies')
    number = models.IntegerField()
    is_checked_out = models.BooleanField(default=False)
    need_to_return = models.BooleanField(default=False)
    booking_date = models.DateField(null=True)
    overdue_date = models.DateField(null=True)
    can_renew = models.BooleanField(default=True, blank=True)

    def is_overdue(self):
        return now() > self.overdue_date

    def overdue(self):
        return now() - self.overdue_date


'''
User is the main predecessor class of all user classes derivatives

User has seventh fields that specifying during creation procedure:
    Login (login) - char field
    Password (password) - char field
    Mail (mail) - email field
    Name (first_name) - char field
    Surname (second_name) - char field
    Address (address) - char field
    Phone number (phone_number) - char field
    Status (status) - char field ('Student' or 'Professor' or another types)
User has field fine that librarian or admin do not specifying during user registration, Zero by default
'''


class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    mail = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    fine = models.IntegerField(default=0, blank=True)
    status = models.CharField(default='Status', max_length=32)


'''
UserCard is a class as a contact information which librarian deals with
Every user has exactly one user card
User card contains all copies, which user checked out

UserCard has three fields that specifying during creation procedure:
    User (user) - relation with certain user, when user is deleting, UserCard deleting with him by cascade deleting
    Library (library) - relation with Library
    Library card number (library_card_number) - integer field, every UserCard has unique library card number, library card number determining based on last existing UserCard library card number
'''


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_card')
    library = models.ForeignKey(Library, default=None, on_delete=models.CASCADE, related_name='user_cards')
    library_card_number = models.IntegerField(default=None)


'''
Patron is the one of three successors of User

Patron has five next unique features:
    Check out (check_out_doc) - feature of check outing the document (standing in queue for a certain document)
    Search (many different searches) - features of searching documents by any criteria
    Renew (renew) - feature of renewing the copy of certain document
    Has overdue (has_overdue) - feature that returns True if Patron has any overdue and False if has not
    Type (type) - feature that returns type of this Patron

Patrons are creating by librarians
'''


class Patron(User):

    def renew(self, copy):
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to renew the copy of document " + copy.document.title)
        if copy.can_renew and self.status != 'Visiting Professor':
            copy.overdue_date += datetime.timedelta(days=7)
            copy.can_renew = False
            copy.save()
            logging.info("Patron " + self.first_name + " " + self.second_name + " renewed the copy of document " + copy.document.title)
        else:
            logging.info("Patron " + self.first_name + " " + self.second_name + " tried to renew the copy of document " + copy.document.title + ", but he cannot do that")

    def search_by_availability(self):  # this search returns all documents which has at least one available copy.
        logging.info("Patron " + self.first_name + self.second_name + " trying to search documents by availability")
        documents = Document.objects.all().filter(copies__is_checked_out=False)
        results_id = [documents.first().id]
        docs = documents[1:]
        i = 0
        for doc in docs:
            if doc.id != results_id[i]:
                results_id.append(doc.id)
                i += 1
        res = Document.objects.all().filter(id__in=results_id)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " documents by availability ")
        return res

    def search_by_title(self, title):  # this search returns all documents which titles contains 'title'.
        # For example, if document has title 'Test', search by 'te' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by title " + title)
        res = Document.objects.all().filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " documents by title " + title)
        return res

    def search_by_titles_and(self, titles):  # this search returns all documents which titles contains words from 'titles'.
        # For example, if document has title 'Test', search by ['tes', 'est'] will return this document too.
        titles_str = ''
        for title in titles:
            titles_str += title
            titles_str += ' and '
        titles_str = titles_str[:-5]
        titles_str += '.'

        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by title " + titles_str)
        res = Document.objects.all()
        for title in titles:
            res = res.filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents " + str(res.count()) + " by title " + titles_str)
        return res

    def search_by_titles_or(self, titles):  # this search returns all documents which titles contains at least one word from 'titles'.
        # For example, if document has title 'Test', search by ['tes', 'just'] will return this document too.
        titles_str = ''
        for title in titles:
            titles_str += title
            titles_str += ' or '
        titles_str = titles_str[:-4]
        titles_str += '.'

        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by title " + titles_str)
        results_id = []
        for title in titles:
            res = Document.objects.all().filter(title__icontains=title)
            for result in res:
                results_id.append(result.id)
        results_id = list(set(results_id))
        res = Document.objects.all().filter(id__in=results_id)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found documents " + str(res.count()) + " by title " + titles_str)
        return res

    def search_by_author(self, author):  # this search returns all documents which authors names contains 'author'.
        # For example, if document has authors 'Tolkien' and 'Rowling', search by 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by author " + author)
        res = Document.objects.all().filter(authors__name__icontains=author)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " documents by author " + author)
        return res

    def search_by_keywords(self, keywords):  # this search returns all documents which keywords contains keywords from 'keywords'.
        # For example, if document has keywords 'key, word', search by 'key' will return this document too.
        keywords_str = ''
        for keyword in keywords:
            keywords_str += keyword.word
            keywords_str += ', '
        keywords_str = keywords_str[:-2]
        keywords_str += '.'

        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by keywords: " + keywords_str)
        res = Document.objects.all().filter(keywords__in=keywords)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " documents by keywords: " + keywords_str)
        return res

    def search_by_title_available(self, title):  # this search returns all available documents which titles contains 'title'.
        # For example, if document has title 'Test' and at least one available copy, search by 'te' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by title " + title)
        res = self.search_by_availability().filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " available documents by title " + title)
        return res

    def search_by_author_available(self, author):  # this search returns all available documents which authors names contains 'author'.
        # For example, if document has authors 'Tolkien' and 'Rowling' and at least one available copy, search by 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by author " + author)
        res = self.search_by_availability().filter(authors__name__icontains=author)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " available documents by author " + author)
        return res

    def search_by_author_and_title(self, title, author):  # this search returns all documents which authors names contains 'author' and titles contains 'title'.
        # For example, if document has title 'Test' and authors 'Tolkien' and 'Rowling', search by 'te', 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search documents by author " + author + " and title " + title)
        res = Document.objects.all().filter(authors__name__icontains=author).filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " documents by author " + author + " and title " + title)
        return res

    def search_by_author_and_title_available(self, author, title):  # this search returns all available documents which authors names contains 'author' and titles contains 'title'.
        # For example, if document has title 'Test' and authors 'Tolkien' and 'Rowling' and at least one available copy, search by 'te', 'tolk' will return this document too.
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to search available documents by author " + author + " and title " + title)
        res = self.search_by_availability().filter(authors__name__icontains=author).filter(title__icontains=title)
        logging.info("Patron " + self.first_name + " " + self.second_name + " found " + str(res.count()) + " available documents by author " + author + " and title " + title)
        return res

    '''Patron cannot check out some copy of the document by himself, so he is just trying to got in queue. If it is not possible returns False'''

    def check_out_doc(self, document):
        logging.info("Patron " + self.first_name + " " + self.second_name + " trying to got in queue for the document " + document.title)
        for copy in self.user_card.copies.all():
            if copy.document.id == document.id:
                # print("You cannot got in queue for this document because you're already have a copy of this document")
                logging.info("Patron " + self.first_name + " " + self.second_name + " cannot got in queue because he is already has a copy of this document")
                return False  # user has already checked this document
        queue = document.queue_type(user=self)
        for user in queue.all():
            if user.id == self.id:
                # print("You cannot got in queue for this document because you're already in this queue")
                logging.info("Patron " + self.first_name + " " + self.second_name + " cannot got in queue because he is already in this queue")
                return False
        queue.add(self)
        logging.info("Patron " + self.first_name + " " + self.second_name + " got in queue for the document " + document.title)
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


'''
Student class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class Student(Patron):
    pass


'''
Faculty class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class Faculty(Patron):
    pass


'''
Visiting professor class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class VisitingProfessor(Patron):
    pass


'''
Instructor class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class Instructor(Faculty):
    pass


'''
TA class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class TA(Faculty):
    pass


'''
Professor class is the successor class of Patron that has not any special fields or features, but his type is using in another features
'''


class Professor(Faculty):
    pass


'''
Librarian class is the successor class of User
Librarian class is the main moderator class of the LMS

Librarian has only one extra field that specifying during creation procedure:
    Level of privileges (level_of_privileges) - integer field
Librarian has many features:
    Handle book (handle_book) handling a copy of book to the certain user if he is first in the queue for this document and this document has any free copy
    Send email (send_email) sending email to the certain user
    Notify (notify) notifying certain user that he has only one day to return the copy of document
    Outstanding request (outstanding_request) placing an outstanding request for the certain document if he has at least second level of privileges
    Accept doc (accept_doc) accepting a copy of certain document from certain patron
    Accept doc after outstanding request (accept_doc_after_outstanding_request) accepting a copy of certain document from certain patron and deleting this copy from database
    Many creating features (create_...) creating many things from database if librarian has at least second level of privileges
    Many deleting features (remove_...) deleting many things from database if librarian has third level of privileges
    Another features using in another features or in front-end
    
Librarians are creating by admin
'''


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
                        copy.overdue_date = copy.booking_date + doc.booking_period(user)
                        copy.can_renew = True
                        queue.remove(user)
                        doc.save()
                        user.user_card.save()
                        user.save()
                        copy.save()
                        logging.info("Librarian " + self.first_name + " " + self.second_name + " handled a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name)
                        return True
                # print("This book has not any available copy")
                logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to handle a copy of document " + doc.title + " to patron " + user.first_name + " " + user.second_name + ", but this document has not any available copy")
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
        # line below commented because we do not want to spam in every test
        # send_mail(subject=subject, message=message, from_email=library.mail, recipient_list=to, fail_silently=False)

    def check_information_of_the_system(self):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to check the information of the system")
        if self.level_of_privileges >= 1:
            # implementation of checking the information of the system maybe will be here (i don't know what this feature should do, because we have not defined technical task for this feature)
            logging.info("Librarian " + self.first_name + " " + self.second_name + " checked the information of the system")
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to check the information of the system, but he has not enough level of privileges")

    def outstanding_request(self, doc):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an outstanding request for the document " + doc.title)
        if self.level_of_privileges >= 2:
            self.remove_all_copies_without_check(doc)
            message = 'Dear user, sorry but you have been removed from the queue on document "' + doc.title + '" due to an outstanding request'
            removed_users_mails = []
            for user in doc.studentsQueue.all():
                removed_users_mails.append(user.mail)
                doc.studentsQueue.remove(user)
            for user in doc.instructorsQueue.all():
                removed_users_mails.append(user.mail)
                doc.instructorsQueue.remove(user)
            for user in doc.TAsQueue.all():
                removed_users_mails.append(user.mail)
                doc.TAsQueue.remove(user)
            for user in doc.professorsQueue.all():
                removed_users_mails.append(user.mail)
                doc.professorsQueue.remove(user)
            for user in doc.visitingProfessorsQueue.all():
                removed_users_mails.append(user.mail)
                doc.visitingProfessorsQueue.remove(user)
            if len(removed_users_mails) > 0:
                self.send_email(message=message, subject='Outstanding request', to=removed_users_mails)
                logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patrons who was removed from deleted queue for the document " + doc.title + " due to an outstanding request")

            message = 'Dear user, please return the copy of "' + doc.title + '" immediately due to an outstanding request. You have only 1 day to return this document'
            users_with_copy = []
            for copy in doc.copies.all():  # we are do not checking copy for is_checked_out because all checked out copies already deleted
                users_with_copy.append(copy.user_card.user.mail)
                copy.overdue_date = datetime.date.today() + datetime.timedelta(days=1)
                copy.can_renew = False
                copy.save()
            if len(users_with_copy) > 0:
                self.send_email(message=message, subject='Outstanding request', to=users_with_copy)
                logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patrons who should to immediately return the document " + doc.title + " due to an outstanding request")
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an outstanding request for the document " + doc.title + ", but he has not enough level of privileges")
            # print("You cannot perform this action")

    def notify(self, user, document):
        message = 'Dear user, you have 1 day to take a copy of ' + document.title + ' you queued up for. After the expiration of this period you will lose this opportunity and will be removed from the queue. Good luck. Your InnoLib'
        self.send_email(message=message, subject='Waiting notification', to=[user.mail])
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
                    if datetime.date.today() > copy.overdue_date:
                        days = (datetime.date.today() - copy.overdue_date).days
                        fine = days * 100
                        if fine > copy.document.price_value:
                            fine = copy.document.price_value
                        user.fine += fine
                        user.save()
                    logging.info("Librarian " + self.first_name + " " + self.second_name + " accepted the copy of document " + doc.title + " from patron " + user.first_name + " " + user.second_name)
                    # first = copy.document.first_in_queue()
                    # self.notify(first, copy.document)
                    logging.info("Librarian " + self.first_name + " " + self.second_name + " notified the patron " + user.first_name + " " + user.second_name + " that now he is first in queue for the document " + doc.title)
                    return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to accept the copy of document " + doc.title + " from patron " + user.first_name + " " + user.second_name + ", but he has not any copy of this document")
        # print("This user has not any copy of this document")
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

    # def check_overdue_copies(self):
    #     for user_card in UserCard.objects.all():
    #         for copy in user_card.copies:
    #             if copy.if_overdue():
    #                 user_card.user.fine += copy.overdue * copy.document.price_value

    def get_or_create_keywords(self, list_of_keywords):
        if self.level_of_privileges >= 2:
            list = []
            for word in list_of_keywords:
                keyword = Keyword.objects.get_or_create(word=word)
                keyword[0].save()
                list.append(keyword[0])
            return list

    def get_or_create_authors(self, list_of_names):
        names = list_of_names[0]
        for i in range(1, len(list_of_names)):
            names += ', '
            names += list_of_names[i]
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an authors: " + names)
        if self.level_of_privileges >= 2:
            list_of_authors = []
            for name in list_of_names:
                author = Author.objects.get_or_create(name=name)
                author[0].save()
                list_of_authors.append(author[0])
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created an authors: " + names)
            return list_of_authors
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an authors: " + names + ", but he has not enough level of privileges")

    def create_author(self, name):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create an author " + name)
        if self.level_of_privileges >= 2:
            author = Author.objects.create(name=name)
            author.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created an author " + name)
            return author
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create an author " + name + ", but he has not enough level of privileges")

    def create_book(self, is_best_seller, reference, title, price_value, edition, publisher, year):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create a book " + title)
        if self.level_of_privileges >= 2:
            library = Library.objects.first()
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created a book " + title)
            return model
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def create_book_new(self, is_best_seller, reference, title, price_value, edition, publisher, year, authors, keywords):
        library = Library.objects.first()
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def create_book_with_authors_names(self, is_best_seller, reference, title, price_value, edition, publisher, year, authors, keywords):
        library = Library.objects.first()
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create a book " + title)
        if self.level_of_privileges >= 2:
            class_model = ReferenceBook if reference else Book
            model = class_model.objects.create(library=library, title=title, price_value=price_value,
                                               is_best_seller=is_best_seller, edition=edition, publisher=publisher,
                                               year=year)
            model.save()
            auth = self.get_or_create_authors(authors)
            for author in auth:
                model.authors.add(author)
            model.save()
            key = self.get_or_create_keywords(keywords)
            for keyword in key:
                model.keywords.add(keyword)
            model.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created a book " + title)
            return model
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create a book" + title + ", but he has not enough level of privileges")
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create " + str(number) + " copies of document " + document.title + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def create_av(self, title, publisher, year, price_value):
        library = Library.objects.first()
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to create AV " + title)
        if self.level_of_privileges >= 2:
            av = AudioVideo.objects.create(library=library, title=title, price_value=price_value, publisher=publisher, year=year)
            av.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " created AV " + title)
            return av
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create AV " + title + ", but he has not enough level of privileges")
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create user " + first_name + " " + second_name + ", but he has not enough level of privileges")
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
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to create " + status + " " + first_name + " " + second_name + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def remove_object(self, obj):
        if isinstance(obj, Patron):
            obj_type = Patron
            logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove patron " + obj.first_name + " " + obj.second_name)
        elif isinstance(obj, Document):
            obj_type = Document
            logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove document " + obj.title)
        elif isinstance(obj, Admin):
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove admin " + obj.first_name + " " + obj.second_name)
            return False
        else:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove not a patron and not an document")
            return False

        if self.level_of_privileges == 3:
            obj.delete()

            if obj_type is Patron:
                logging.info("Librarian " + self.first_name + " " + self.second_name + " removed patron " + obj.first_name + " " + obj.second_name)
            elif obj_type is Document:
                logging.info("Librarian " + self.first_name + " " + self.second_name + " removed document " + obj.title)
            return True

        if obj_type is Patron:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove patron " + obj.first_name + " " + obj.second_name + ", but he has not enough level of privileges")
        elif obj_type is Document:
            logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove document " + obj.title + ", but he has not enough level of privileges")

    def remove_copies(self, document, count):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove " + str(count) + " copies of document " + document.title)
        if self.level_of_privileges == 3:
            if count > document.copies.count():
                logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove " + str(count) + " copies of document " + document.title + ", but this document has not so much copies")
                return False
            amount = count
            for copy in document.copies.all():
                if not copy.is_checked_out:
                    copy.delete()
                    amount -= 1
                    if amount == 0:
                        break
            document.save()
            for copy in document.copies.all():
                copy.number -= count
                copy.save()
            document.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " removed " + str(count) + " copies of document " + document.title)
            return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove " + str(count) + " copies of document " + document.title + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def remove_all_copies(self, document):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove all copies of document " + document.title)
        if self.level_of_privileges == 3:
            for copy in document.copies.all():
                if not copy.is_checked_out:
                    copy.delete()
            document.save()
            logging.info("Librarian " + self.first_name + " " + self.second_name + " removed all copies of document " + document.title)
            return True
        logging.info("Librarian " + self.first_name + " " + self.second_name + " tried to remove all copies of document " + document.title + ", but he has not enough level of privileges")
        # print("You cannot perform this action")

    def remove_all_copies_without_check(self, document):
        logging.info("Librarian " + self.first_name + " " + self.second_name + " trying to remove all copies of document " + document.title + " without check")
        for copy in document.copies.all():
            if not copy.is_checked_out:
                copy.delete()
        document.save()
        logging.info("Librarian " + self.first_name + " " + self.second_name + " removed all copies of document " + document.title + " without check")

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


'''
Admin class is the successor class of User class
Admin is the main moderator class of LMS
Admin has 4 unique moderating features:
    Add librarian (add_librarian) that creating librarian in database
    Change level of privileges (change_level_of_privileges) that changing the level of privileges of certain librarian in database
    Delete librarian (delete_librarian) that deleting certain librarian from database
    Check logs (check_logs) that returns all saved logs by string
Admin has 1 extra feature for tests:
    Check logs for tests (check_logs_for_tests) that printing all saved logs after certain line
Admin creating by library at the starting work of LMS
There is could be only one admin in database
'''


class Admin(User):

    def add_librarian(self, first_name, second_name, login, password, address, phone_number, mail, level_of_privileges):
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to add librarian " + first_name + " " + second_name)
        library_card_number = User.objects.last().user_card.library_card_number + 1
        librarian = Librarian.objects.create(first_name=first_name, second_name=second_name, login=login, password=password,
                                             address=address, phone_number=phone_number, mail=mail, level_of_privileges=level_of_privileges, status='Librarian')
        user_card = UserCard.objects.create(user=librarian, library=self.user_card.library, library_card_number=library_card_number)
        librarian.save()
        user_card.save()
        logging.info("Admin " + self.first_name + " " + self.second_name + " added librarian " + first_name + " " + second_name)
        return librarian

    def change_level_of_privileges(self, librarian, level_of_privileges):
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to change level of privileges of librarian " + librarian.first_name + " " + librarian.second_name)
        librarian.level_of_privileges = level_of_privileges
        logging.info("Admin " + self.first_name + " " + self.second_name + " changed level of privileges of librarian " + librarian.first_name + " " + librarian.second_name)

    def delete_librarian(self, librarian):
        logging.info("Admin " + self.first_name + " " + self.second_name + " trying to delete librarian " + librarian.first_name + " " + librarian.second_name)
        librarian.delete()
        logging.info("Admin " + self.first_name + " " + self.second_name + " deleted librarian " + librarian.first_name + " " + librarian.second_name)

    def check_logs(self):
        return open("InnoLib.log", "r").read()

    def check_logs_for_tests(self, string):
        logs = open("InnoLib.log", "r")
        for line in logs:
            if line.endswith(string, 50, -1):
                break
        for line in logs:
            print(line)
