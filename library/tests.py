import datetime
from django.test import TestCase
from library.models import *


def create_library():
    return Library.objects.create()


def create_user(self,class_model, library, num):
    return User.objects.create(login='test', password='test', first_name='test', second_name='test',address='test', phone_number='test', library_card_number=num, library=library)


def create_p1(self,library):
    return Faculty.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
                                  address="Via Margutta, 3", phone_number='30001', library_card_number=1010,
                                  library=library)


def create_p2(self,library):
    return Student.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                  address="Via Sacra, 13", phone_number='30002', library_card_number=1011, library=library)


def create_p3(self,library):
    return Student.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                  address="Via del Corso, 22", phone_number='30003', library_card_number=1100, library=library)


def create_book(self,library, is_best_seller=False, reference=False, title='"Good_book"'):
    class_model = ReferenceBook if reference else Book
    return class_model.objects.create(library=library, title=title, price_value=0, is_best_seller=is_best_seller,
                                      edition='0', publisher='test', year=2000)


def create_b1(self,library):
    return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0, is_best_seller=False,
                                      edition="Third edition", publisher='MIT Press', year=2009)


def create_b2(self,library):
    return Book.objects.create(library=library, title="Design Patterns: Elements of Reusable Object-Oriented Software",
                               price_value=0, is_best_seller=True, edition="First edition",
                               publisher="Addison-Wesley Professional", year=2003)


def create_b3(self,library):
    return ReferenceBook.objects.create(library=library, title="The Mythical Man-month", price_value=0,
                                        is_best_seller=False, edition="Second edition",
                                        publisher="Addison-Wesley Longman Publishing Co., Inc", year=1995)


def create_copy(self, document, number):
    Copy.objects.create(document=document, number=number)


def create_author(self):
    return Author.objects.create(name='Unnamed_author')


def create_av(self,library, title="Test"):
    return AudioVideo.objects.create(library=library, title=title, price_value=0)


def create_av1(self,library):
    return AudioVideo.objects.create(library=library, title="Null References: The Billion Dollar Mistake", price_value=0)


def create_av2(self,library):
    return AudioVideo.objects.create(library=library, title="Information Entropy", price_value=0)
"""""
class FirstTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Librarian, lib, 1)
        book = create_book(self,lib, is_best_seller=False, reference=False, title='"Good_book"')
        create_copy(book, 0)
        create_copy(book, 1)

    def test_case(self):
        print("TEST 1")
        patron = Patron.objects.get()
        book = Book.objects.get()
        lib = Library.objects.get()
        if patron.check_out_doc(book):
            print("patron checked out the book " + book.title)
        else:
            print("patron can't check out the book " + book.title)
        print("patron has " + str(len(Copy.objects.filter(document=book, is_checked_out=True,
                                                          user=patron))) + ' copies of the book "' + book.title + '"')
        print("library has " + str(lib.count_unchecked_copies(book)) + ' unchecked copies of the book "' + book.title)


class SecondTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Librarian, lib, 1)
        create_author(self)

    def test_case(self):
        print("TEST 2")
        patron = Patron.objects.get()
        author = Author.objects.get()
        if Document.objects.filter(authors=author).exists():
            print("library has books of author " + author.name)
        else:
            print("library has no books of author " + author.name)


class ThirdTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Faculty, lib, 0)
        create_user(Student, lib, 1)
        create_user(Librarian, lib, 2)
        book = create_book(self,lib)
        create_copy(self, book, 0)

    def test_case(self):
        print("TEST 3")
        faculty = Faculty.objects.get()
        book = Book.objects.get()
        if faculty.check_out_doc(book):
            print("faculty checked out the book successfully")
        else:
            print("faculty didn't check out the book")
        copy = Copy.objects.get()
        print("returning time is: " + str((copy.overdue_date - copy.booking_date).days) + " days")


class FourthTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Faculty, lib, 0)
        create_user(Student, lib, 1)
        create_user(Librarian, lib, 2)
        book = create_book(self,lib, is_best_seller=True)
        create_copy(self, book, 0)

    def test_case(self):
        print("TEST 4")
        faculty = Faculty.objects.get()
        book = Book.objects.get()
        if faculty.check_out_doc(book):
            print("faculty checks out the book successfully")
        else:
            print("faculty didn't check out the book")
        copy = Copy.objects.get()
        print("returning time is: " + str((copy.overdue_date - copy.booking_date).days) + " days")


class FifthTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Patron, lib, 1)
        create_user(Patron, lib, 2)
        create_user(Librarian, lib, 3)
        book = create_book(self, lib)
        create_copy(self, book, 0)
        create_copy(self, book, 1)

    def test_case(self):
        print("TEST 5")
        patron1, patron2, patron3 = Patron.objects.all()
        book = Book.objects.get()
        if patron1.check_out_doc(book):
            print("patron #" + str(patron1.library_card_number) + " checks out the book " + book.title)
        else:
            print("patron #" + str(patron1.library_card_number) + " can't check out the book " + book.title)

        if patron2.check_out_doc(book):
            print("patron #" + str(patron2.library_card_number) + " checks out the book " + book.title)
        else:
            print("patron #" + str(patron2.library_card_number) + " can't check out the book " + book.title)

        if patron3.check_out_doc(book):
            print("patron #" + str(patron3.library_card_number) + " checks out the book " + book.title)
        else:
            print("patron #" + str(patron3.library_card_number) + " can't check out the book " + book.title)


class SixthTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Librarian, lib, 1)
        book = create_book(self, lib)
        create_copy(self, book, 0)
        create_copy(self, book, 1)

    def test_case(self):
        print("TEST 6")
        patron = Patron.objects.get()
        book = Book.objects.get()
        print("patron tries to check out the book " + book.title)
        if patron.check_out_doc(book):
            print("patron checks out the book " + book.title)
        else:
            print("patron can't check out the book " + book.title)

        print("patron tries to check out the book " + book.title)
        if patron.check_out_doc(book):
            print("patron checks out the book " + book.title)
        else:
            print("patron can't check out the book " + book.title)


class SeventhTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Patron, lib, 1)
        create_user(Librarian, lib, 2)
        book = create_book(self, lib)
        create_copy(self, book, 0)
        create_copy(self, book, 1)

    def test_case(self):
        print("TEST 7")
        patron1, patron2 = Patron.objects.all()
        book = Book.objects.get()
        patron1.check_out_doc(book)
        patron2.check_out_doc(book)

        if Copy.objects.filter(document=book, is_checked_out=True, user=patron1).exists():
            print("Patron # " + str(patron1.library_card_number) + " has copy of the book " + book.title)
        else:
            print("Patron # " + str(patron1.library_card_number) + " hasn't copy of the book " + book.title)

        if Copy.objects.filter(document=book, is_checked_out=True, user=patron2).exists():
            print("Patron # " + str(patron2.library_card_number) + " has copy of the book " + book.title)
        else:
            print("Patron # " + str(patron2.library_card_number) + " hasn't copy of the book " + book.title)


class EighthTestCase(TestCase):
    def setUp(self):

        lib = create_library()
        create_user(Faculty, lib, 0)
        create_user(Student, lib, 1)
        create_user(Librarian, lib, 2)
        book = create_book(self, lib)
        create_copy(self, book, 0)

    def test_case(self):
        print("TEST 8")
        student = Student.objects.get()
        book = Book.objects.get()
        print("student tries to check out the book " + book.title)
        student.check_out_doc(book)
        if Copy.objects.filter(document=book, is_checked_out=True, user=student).exists():
            print("Patron has copy of the book " + book.title)
        else:
            print("Student hasn't copy of the book " + book.title)
        copy = Copy.objects.get()
        print("returning time is: " + str((copy.overdue_date - copy.booking_date).days) + " days")


class NinthTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Faculty, lib, 0)
        create_user(Student, lib, 1)
        create_user(Librarian, lib, 2)
        book = create_book(self, lib, is_best_seller=True)
        create_copy(self, book, 0)

    def test_case(self):
        print("TEST 9")
        student = Student.objects.get()
        book = Book.objects.get()
        print("student tries to check out the book " + book.title)
        student.check_out_doc(book)
        if Copy.objects.filter(document=book, is_checked_out=True, user=student).exists():
            print("Patron has copy of the book " + book.title)
        else:
            print("Student hasn't copy of the book " + book.title)
        copy = Copy.objects.get()
        print("returning time is: " + str((copy.overdue_date - copy.booking_date).days) + " days")


class TenthTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Librarian, lib, 1)
        book_a = create_book(self, lib, title='A')
        create_copy(self, book_a, 0)
        book_b = create_book(self, lib, reference=True, title="B")
        create_copy(self, book_b, 0)

    def test_case(self):
        print("TEST 10")
        patron = Patron.objects.get()
        book_a = Book.objects.get(title='A')
        book_b = ReferenceBook.objects.get()

        print("patron tries to check out the book " + book_a.title)
        if patron.check_out_doc(book_a):
            print("patron checks out the book " + book_a.title)
        else:
            print("patron can't check out the book " + book_a.title)

        print("patron tries to check out the book " + book_b.title)
        if patron.check_out_doc(book_b):
            print("patron checks out the book " + book_b.title)
        else:
            print("patron can't check out the book " + book_b.title)
"""

#def create_user(self,class_model, library, num):
 #   return User.objects.create(login='test', password='test', first_name='test', second_name='test',address='test', phone_number='test', library_card_number=5, library=library)

class FirstTestCase(TestCase):
    def setUp(self):
        library = create_library()
        librarian = create_user(self,class_model=Librarian,num=5, library = library)

    def testCase(self):
        print("Test 1")
        library = Library.objects.get(1)
        librarian = Librarian.objects.get(1)

        b1 = librarian.create_b1(self, library)
        librarian.create_copy(b1, 3)
        b2 = librarian.create_b2(self, library)
        librarian.create_copy(b2, 2)
        b3 = librarian.create_b3(self, library)
        librarian.create_copy(b3, 1)

        av1 = librarian.create_av1(library)
        av2 = librarian.create_av2(library)

        p1 = librarian.create_p1(library)
        p2 = librarian.create_p2(library)
        p3 = librarian.create_p3(library)

        print("The number of documents in the System is " + Document.objects.count() +
              "and the number of users is " + User.objects.count())

    def setDown(self):
        Patron.objects.all.delete()
        AudioVideo.objects.all.delete()
        Copy.objects.all.delete()
        Book.objects.all.delete()
        Library.objects.all.delete()
        Librarian.objects.all.delete()


class SecondTestCase(TestCase):
    def setUp(self):
        FirstTestCase.setUp(self)
        FirstTestCase.testCase(self)

    def testCase(self):
        print("Test 2")
        librarian = Librarian.objects.get(1)
        b1 = Book.objects.get(1)
        b3 = Book.objects.get(3)

        librarian.remove_copy(b1, 2)
        librarian.remove_copy(b3, 1)
        librarian.remove_patron(2)

        print("The number of documents in the System is " + Document.objects.count() +
              "and the number of users is " + User.objects.count())

    def setDown(self):
        FirstTestCase.setDown(self)


class ThirdTestCase(TestCase):
    def setUp(self):
        FirstTestCase.setUp(self)
        FirstTestCase.testCase(self)

    def testCase(self):
        print("Test 3")
        librarian = Librarian.objects.get(1)

        librarian.patron_information(1)
        librarian.patron_information(3)

    def setDown(self):
        FirstTestCase.setDown(self)


class FourthTestCase(TestCase):
    def setUp(self):
        SecondTestCase.setUp(self)
        SecondTestCase.testCase(self)

    def testCase(self):
        print("Test 4")
        librarian = Librarian.objects.get(1)
        librarian.patron_information(2)
        librarian.patron_information(3)

    def setDown(self):
        FirstTestCase.setDown(self)


class FifthTestCase(TestCase):
    def setUp(self):
        SecondTestCase.setUp(self)
        SecondTestCase.testCase(self)

    def testCase(self):
        print("Test 5")
        p2 = Patron.objects.get(2)
        b1 = Book.objects.get(1)
        if p2.in_library():
            p2.check_out_doc(b1)
        else:
            print("p2 is not a patron of the library hence he cannot check out any document.")

    def setDown(self):
        FirstTestCase.setDown(self)


class SixthTestCase(TestCase):
    def setUp(self):
        SecondTestCase.setUp(self)
        SecondTestCase.testCase(self)

    def testCase(self):
        print("Test 6")
        librarian = Librarian.objects.get(1)
        b1 = Book.objects.get(1)
        b2 = Book.objects.get(2)
        p1 = Patron.objects.get(1)
        p3 = Patron.objects.get(3)
        p1.check_out_doc(b1)
        p3.check_out_doc(b1)
        p3.check_out_doc(b2)
        librarian.patron_information(1)
        librarian.patron_information(3)

    def setDown(self):
        FirstTestCase.setDown(self)


class SeventhTestCase(TestCase):
    def setUp(self):
        FirstTestCase.setUp(self)
        FirstTestCase.testCase(self)

    def testCase(self):
        librarian = Librarian.objects.get(1)
        b1 = Book.objects.get(1)
        b2 = Book.objects.get(2)
        b3 = Book.objects.get(3)
        p1 = Patron.objects.get(1)
        p2 = Patron.objects.get(2)
        p3 = Patron.objects.get(3)
        av1 = AudioVideo.objects.get(1)
        av2 = AudioVideo.objects.get(2)

        p1.check_out_doc(b1)
        p1.check_out_doc(b2)
        p1.check_out_doc(b3)
        p1.check_out_doc(av1)
        p2.check_out_doc(b1)
        p2.check_out_doc(b2)
        p2.check_out_doc(av2)
        librarian.patron_information(1)
        librarian.patron_information(2)


# class EighthTestCase(TestCase):
#     def setUp(self):
#         FirstTestCase.setUp()
#         FirstTestCase.testCase()
#
#         b1 = Book.objects.get(1)
#         b2 = Book.objects.get(2)
#         p1 = Patron.objects.get(1)
#         p2 = Patron.objects.get(2)
#         av1 = AudioVideo.objects.get(1)
#
#         datetime.date = 02.09
#         p1.check_out_doc(b1)
#         datetime.date = 02.02
#         p1.check_out_doc(b2)
#         datetime.date = 02.05
#         p2.check_out_doc(b1)
#         datetime.date = 02.17
#         p2.check_out_doc(av1)
#
#     def testCase(self):
#         librarian = Librarian.objects.get(1)
#         p1 = Patron.objects.get(1)
#         p2 = Patron.objects.get(2)
#
#         datetime.date = 03.05
#
#         print("p1  Overdue: [(", end='')
#         for copy in p1.user_card.copies:
#             if copy.overdue_date > datetime.date:
#                 print("b2,", datetime.datetime - copy.overdue_date, "days")
#
#     def setDown(self):
#         FirstTestCase.setDown()


class NinthTestCase(TestCase):
    def setUp(self):
        FirstTestCase.setUp(self)

    def testCase(self):
        FirstTestCase.testCase(self)
