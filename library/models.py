from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import datetime
import re


class Library(models.Model):
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
    username = models.EmailField()
    password = models.CharField(max_length=128)


# All the classes below (but not copy) are about documents. Copy connects library and documents


class Author(models.Model):
    name = models.CharField(max_length=250)


class Keyword(models.Model):
    word = models.CharField(max_length=255)


# There are 3 types of documents: books, journal articles and audio/video files
class Document(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='documents')
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, related_name='documents')
    price_value = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='documents')
    usersQueue = models.ManyToManyField("Patron", related_name='documents')

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)


class Book(Document):
    is_best_seller = models.BooleanField(default=False)
    edition = models.CharField(max_length=63)
    publisher = models.CharField(max_length=63)
    year = models.IntegerField()

    def booking_period(self, user):
        if isinstance(user, Faculty):
            return datetime.timedelta(weeks=4)
        elif self.is_best_seller:
            return datetime.timedelta(weeks=2)
        return datetime.timedelta(weeks=3)


class ReferenceBook(Book):
    authors = models.ManyToManyField(Author, related_name='reference')
    keywords = models.ManyToManyField(Keyword, related_name='reference')

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)


class AudioVideo(Document):

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)


class Editor(models.Model):
    first_name = models.CharField(max_length=250)
    second_name = models.CharField(max_length=250)


class Journal(models.Model):
    title = models.CharField(max_length=250)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='journals')
    authors = models.ManyToManyField(Author, related_name='journals')
    price_value = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='journals')

    def booking_period(self, user):
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

    def check_out(self, user):
        if isinstance(self.document, ReferenceBook):
            return False
        if self.document.copies.filter(user=user).exists():
            return False
        self.is_checked_out = True
        self.user = user
        self.booking_date = datetime.date.today()
        self.overdue_date = self.booking_date + self.document.booking_period(user)
        self.save()
        return True


# All the classes below are about users


# there are 2 types of users: patrons and librarians
class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_card')
    library_card_number = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='user_cards')
    copies = models.ManyToManyField(Copy)


# there are 2 types of patrons: students and faculties
class Patron(User):

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
        for copy in document.copies.all():
            if not copy.is_checked_out:
                copy.is_checked_out = True
                self.user_card.copies.add(copy)
                copy.booking_date = datetime.date.today()
                self.user_card.save()
                copy.save()
                return True
        document.usersQueue.put(self)
        return False  # there are no available copies

    # return copy of the document to the library. If it is not possible returns False
    def return_doc(self, document):
        for copy in self.user_card.copies.all():
            if copy.document == document:
                self.user_card.copies.exclude(copy)
                self.user_card.save()
                Librarian.objects.get(id='1').handed_over_copies.add(copy)
                return True
        return False  # no such document

    def has_overdue(self):  # bool
        for copy in self.user_card.copies.all():
            if copy.overdue_date > datetime.date:
                return True
        return False


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


class Librarian(User):  # (User,UserCard)

    handed_over_copies = models.ManyToManyField(Document)

    def accept_doc(self, copy):
        copy.is_checked_out = False
        copy.save()
        self.handed_over_copies.remove(copy)

    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.all())

    def is_due(self):
        pass

    def overdue_fines(self):
        pass

    def patrons_docs(self, user, doc):
        for copy in user.user_card.copies.all():
            if copy.document == doc:
                print(user.first_name + " " + user.second_name + ": " + doc.title + ": " + copy.number)

    # def unchecked_copies(self, doc):
    #     print("there are " + self.user_card.library.count_unchecked_copies(
    #         doc) + "unchecked copies of document " + doc.title + "in library.")

    def manage_patron(self):
        pass

    def check_overdue_copy(self):
        pass

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
