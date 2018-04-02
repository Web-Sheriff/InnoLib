from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.timezone import now
import datetime
import re


class Library(models.Model):

    mail = models.EmailField(default='test@gmail.com', max_length=64)

    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.all())

    def is_due(self):
        pass

    def overdue_fines(self):
        pass


''' 
every user has exactly one user card
user card contains all copies, which user checked out
user card has unique number
'''


class Login(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


# All the classes below (but not copy) are about documents. Copy connects library and documents


class Author(models.Model):
    name = models.CharField(max_length=64)


class Keyword(models.Model):
    word = models.CharField(max_length=255)


# There are 3 types of documents: books, journal articles and audio/video files
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

    def sort_queue(self):
        pass

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
        else:
            return doc.professorsQueue.first()


class Book(Document):
    is_best_seller = models.BooleanField(default=False)
    edition = models.CharField(max_length=128)
    publisher = models.CharField(max_length=64)
    year = models.IntegerField()

    def booking_period(self, user):
        if self.is_best_seller:
            return datetime.timedelta(weeks=2)
        if isinstance(user, Faculty):
            return datetime.timedelta(weeks=4)
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(weeks=1)
        return datetime.timedelta(weeks=3)


class ReferenceBook(Book):
    authors = models.ManyToManyField(Author, related_name='reference')
    keywords = models.ManyToManyField(Keyword, related_name='reference')


class AudioVideo(Document):

    def booking_period(self, user):
        if isinstance(user, VisitingProfessor):
            return datetime.timedelta(weeks=1)
        return datetime.timedelta(weeks=2)


class Editor(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)


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


class Issue(models.Model):
    publication_date = models.DateField()
    editors = models.ManyToManyField(Editor, related_name='issues')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='issues')


class JournalArticles(Document):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='journal_articles')


class Copy(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, related_name='copies')
    number = models.IntegerField()
    is_checked_out = models.BooleanField(default=False)
    need_to_return = models.BooleanField(default=False)
    booking_date = models.DateField(null=True)
    overdue_date = models.DateField(null=True)
    renew = models.ForeignKey("Librarian",on_delete=models.DO_NOTHING, related_name='renew')
    weeks_renew = models.ForeignKey("Librarian", on_delete=models.DO_NOTHING, related_name='weeks_renew')

    def check_out(self, user):
        if isinstance(self.document, ReferenceBook):
            return False
        if not self.document.copies.filter(user=user).exists():
            return False
        self.is_checked_out = True
        self.user = user
        self.booking_date = datetime.date.today()
        self.overdue_date = self.booking_date + self.document.booking_period(user)
        self.save()
        return True

    def if_overdue(self):
        return datetime.now() > self.overdue_date

    def overdue(self):
        return datetime.now() - self.overdue_date


# All the classes below are about users


# there are 2 types of users: patrons and librarians
class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    mail = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    fine = models.IntegerField()


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_card')
    library_card_number = models.CharField(max_length=128)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='user_cards')
    copies = models.ManyToManyField(Copy)


class AvailableDocs(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='available_documents')
    document = models.OneToOneField(Document, on_delete=models.DO_NOTHING)
    rights_date = models.DateField(now())

    def check_date(self):
        if self.rights_date != datetime.date.today():
            queue = Document.queue_type(doc=self.document, user=self.user)
            queue.exclude(user_card=self.user.user_card)
            queue.model.save()
            self.user.available_documents.exclude(document=self.document, user=self.user)
            self.user.available_documents.model.save()
            first = Document.first_in_queue(doc=self.document)
            first.available_documents.create(document=self.document, user=first)
            Librarian.notify(user=first, document=self.document)


# there are 3 types of patrons: students, faculties and visiting professors
class Patron(User):

    #renew the document for n weeks
    def renew(self, weeks, queue = Copy.renew):  # 13 requirement
        queue.add(self)
        queue.models.save

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
        queue = Document.queue_type(doc=document, user=self)
        if document.studentsQueue.count() + document.TAsQueue.count() + document.instructorsQueue.count() + document.visitingProfessorsQueue.count() + document.professorsQueue.count() > 0:
            queue.add(self)
            queue.model.save()
        for copy in document.copies.all():
            if not copy.is_checked_out:
                for doc in self.available_documents.objects.all():
                    if document.id == doc.id:
                        copy.is_checked_out = True
                        self.user_card.copies.add(copy)
                        copy.booking_date = datetime.date.today()
                        queue.exclude(user_card=self.user_card)
                        queue.model.save()
                        self.user_card.save()
                        copy.save()
                        return True
                CheckOutRequest.objects.create(user_card=self.user_card, copy=copy)
                return True
        return False  # there are no available copies

    # return copy of the document to the library. If it is not possible returns False
    def return_doc(self, document):
        for copy in self.user_card.copies.all():
            if copy.document == document:
                HandOverRequest.objects.create(user_card=self.user_card, copy=copy)
                # self.user_card.copies.exclude(copy)
                # self.user_card.save()
                # Librarian.handed_over_copies.add(copy)
                return True
        return False  # no such document

    def has_overdue(self):  # bool
        for copy in self.user_card.copies.all():
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
            return "VisitingProfessor"


class Student(Patron):
    pass


class Faculty(Patron):
    def faculty_card(self, login, password, name):
        new_fac = Faculty()
        new_fac.login = login
        new_fac.password = password
        new_fac.name = name


class VisitingProfessor(Patron):
    pass


class Instructor(Faculty):
    pass


class TA(Faculty):
    pass


class Professor(Faculty):
    pass


class CheckOutRequest(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.DO_NOTHING, related_name='check_out_request')
    copy = models.ForeignKey(Copy, on_delete=models.DO_NOTHING, related_name='check_out_request')


class HandOverRequest(models.Model):
    user_card = models.ForeignKey(UserCard, on_delete=models.DO_NOTHING, related_name='hand_over_request')
    copy = models.ForeignKey(Copy, on_delete=models.DO_NOTHING, related_name='hand_over_request')


class Librarian(User):

    def renew_request(self):
        for renew in Copy.objects.all():
            weeks = renew.weeks_renew
            delta = datetime.timedelta(days=weeks//7)
            renew.overdue_date += delta


    def outstanding_request(self, request):
        request.copy.is_checked_out = True
        request.user_card.copies.add(request.copy)
        request.copy.booking_date = datetime.date.today()
        request.user_card.save()
        request.copy.save()

    def notify(self, user, document):
        user.available_documents.create(document=document, user=user)
        send_mail(message='Dear user, you have 1 day to take a copy of document you queued up for. After the expiration of this period you will lose this opportunity and will be removed from the queue. Good luck. Your InnoLib',
                  subject='Waiting notification', from_email=Library.mail, recipient_list=user.mail)

    def accept_doc(self, request):
        request.copy.is_checked_out = False
        request.user_card.copies.exclude(request.copy)
        request.user_card.save()
        request.copy.save()

        first = Document.first_in_queue(doc=request.copy.document)
        self.notify(first, request.copy.document)

    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.all())

    def is_due(self):
        pass

    def overdue_fines(self):
        pass

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

    # def unchecked_copies(self, doc):
    #     print("there are " + self.user_card.library.count_unchecked_copies(
    #         doc) + "unchecked copies of document " + doc.title + "in library.")

    def manage_patron(self):
        pass

    def check_overdue_copies(self):
        for card in UserCard.objects:
            for copy in card.copies:
                if copy.if_overdue():
                    card.user.fine += copy.overdue*copy.document.price_value


    def create_book(self, library, is_best_seller, reference, title):
        class_model = ReferenceBook if reference else Book
        return class_model.objects.create(library=library, title=title, price_value=0, is_best_seller=is_best_seller,
                                          edition=0, publisher='test', publish_time=datetime.date.today())

    def create_copy(self, document, number):
        Copy.objects.create(document=document, number=number)

    def create_av(self, library, title):
        return AudioVideo.objects.create(library=library, title=title, price_value=0)

    def add_doc(self):
        pass

    def remove_copy(self, document, count):
        removable = Copy.objects.get(document=document)
        if removable.number > count:
            removable.number -= count
        else:
            removable.delete()

    def patron_information(self, id):
        try:
            patron = Patron.objects.get(id=id)
        except ObjectDoesNotExist:
            print("p", id, ": information no available, patron does not exist.", sep='')
            return
        print("p", id, sep='')
        print(" Name:", patron.first_name, patron.second_name)
        print(" Address:", patron.address)
        print(" Phone Number:", patron.phone_number)
        print(" Lib. card ID:", patron.user_card.id)

        if isinstance(patron, Faculty):
            print(" Type: Faculty")
        else:
            print(" Type: Student")

        print(" (document checked-out, due date): ")
        print("[", end='')

        copies = patron.user_card.copies
        for copy in copies.all():
            if isinstance(copy.document, AudioVideo):
                print("(av", copy.document.id, ',', copy.overdue_date, ')', sep='', end='')
            else:
                print("(b", copy.document.id, ',', copy.overdue_date, ')', sep='', end='')
                if copy != copies.last():
                    print(", ", end='')
        print("]")

    def remove_patron(self, id):
        Copy.objects.get(id).delete()

    def modify_doc(self):
        pass

    def create_user(self, class_model, library, num):
        return class_model.objects.create(login='test',
                                          password='test', first_name='test',
                                          second_name='test', address='test',
                                          phone_number='test', library_card_number=num,
                                          library=library)

    # for tests

    def create_p1(self, library):
        return Faculty.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
                                      address="Via Margutta, 3", phone_number='30001', library_card_number='1010',
                                      library=library)

    def create_p2(self, library):
        return Student.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                      address="Via Sacra, 13", phone_number='30002', library_card_number='1011',
                                      library=library)

    def create_p3(self, library):
        return Student.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                      address="Via del Corso, 22", phone_number='30003', library_card_number='1100',
                                      library=library)

    def create_b1(self, library):
        return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0,
                                   is_best_seller=False,
                                   edition="Third edition", publisher='MIT Press', year=2009)

    def create_b2(self, library):
        return Book.objects.create(library=library,
                                   title="Design Patterns: Elements of Reusable Object-Oriented Software",
                                   price_value=0, is_best_seller=True, edition="First edition",
                                   publisher="Addison-Wesley Professional", year=2003)

    def create_b3(self, library):
        return ReferenceBook.objects.create(library=library, title="The Mythical Man-month", price_value=0,
                                            is_best_seller=False, edition="Second edition",
                                            publisher="Addison-Wesley Longman Publishing Co., Inc", year=1995)

    def create_av1(self, library):
        return AudioVideo.objects.create(library=library, title="Null References: The Billion Dollar Mistake",
                                         price_value=0)

    def create_av2(self, library):
        return AudioVideo.objects.create(library=library, title="Information Entropy", price_value=0)

    def user_card(self, login, password, first_name, second_name, address, phone_number, fac_or_stu):
        new_user = User()
        new_user.login = login
        new_user.password = password
        new_user.first_name = first_name
        new_user.second_name = second_name
        new_user.address = address
        new_user.phone_number = phone_number
        new_user.fac_or_stu = fac_or_stu

    # user story 4
    def list_of_users(self, user):
        for i in user.user_card.copies.all:
            print(i)

    # user story 10
    # def number_of_cards(self, user, n):
    #     for i in n:
    #         create_user(class_model, library, i)

    # user story 11

    # def edit_user(self, class_model, num, login, password, first_name, second_name, address, phone_number, fac_or_stu):
    #     emp = User.objects.get(pk=num)
    #     emp.login = request.POST.get(login)
    #     emp.password = request.POST.get(password)
    #     emp.first_name = request.POST.get(first_name)
    #     emp.second_name = request.POST.get(second_name)
    #     emp.address = request.POST.get(address)
    #     emp.phone_number = request.POST.get(phone_number)
    #     emp.save()

    # user story 14
    # def delete_book(self, library):
    #     return class_model.objects.delete

    # user story 16
    # def return_checked(self, doc):
    #     for i in doc.copies.filter(is_checked_out=True):
    #         if i.has_overdue:
    #             i.need_to_return = True
    #         return doc.copies.filter(is_checked_out=True)

    # def user_card8(self, new_user, new_lib_card, new_lib):
    #     UserCard.user = new_user
    #     UserCard.library = new_lib_card
    #     UserCard.library_card_number = new_lib_card
