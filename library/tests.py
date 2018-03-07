import datetime
from django.test import TestCase
from library.models import *


def create_library():
    return Library.objects.create()


def create_user(class_model, library, num):
    user = class_model.objects.create(login='test', password='test', first_name='test', second_name='test',
                                      address='test', phone_number='test')
    UserCard.objects.create(user=user, library_card_number=num, library=library)
    return user


def create_p1(library):
    user = Faculty.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
                                  address="Via Margutta, 3", phone_number='30001')
    UserCard.objects.create(user=user, library_card_number=1010, library=library)
    return user


def create_p2(library):
    user = Student.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                  address="Via Sacra, 13", phone_number='30002')
    UserCard.objects.create(user=user, library_card_number=1011, library=library)
    return user


def create_p3(library):
    user = Student.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                  address="Via del Corso, 22", phone_number='30003')
    UserCard.objects.create(user=user, library_card_number=1100, library=library)
    return user


def create_book(library, is_best_seller=False, reference=False, title='"Good_book"'):
    class_model = ReferenceBook if reference else Book
    return class_model.objects.create(library=library, title=title, price_value=0, is_best_seller=is_best_seller,
                                      edition='0', publisher='test', year=2000)


def create_b1(library):
    return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0, is_best_seller=False,
                                      edition="Third edition", publisher='MIT Press', year=2009)


def create_b2(library):
    return Book.objects.create(library=library, title="Design Patterns: Elements of Reusable Object-Oriented Software",
                               price_value=0, is_best_seller=True, edition="First edition",
                               publisher="Addison-Wesley Professional", year=2003)


def create_b3(library):
    return ReferenceBook.objects.create(library=library, title="The Mythical Man-month", price_value=0,
                                        is_best_seller=False, edition="Second edition",
                                        publisher="Addison-Wesley Longman Publishing Co., Inc", year=1995)


def create_copy(document, number):
    Copy.objects.create(document=document, number=number)


def create_author():
    return Author.objects.create(name='Unnamed_author')


def create_av(library, title="Test"):
    return AudioVideo.objects.create(library=library, title=title, price_value=0)


def create_av1(library):
    return AudioVideo.objects.create(library=library, title="Null References: The Billion Dollar Mistake", price_value=0)


def create_av2(library):
    return AudioVideo.objects.create(library=library, title="Information Entropy", price_value=0)


"""
class FirstTestCase(TestCase):
    def setUp(self):
        lib = create_library()
        create_user(Patron, lib, 0)
        create_user(Librarian, lib, 1)
        book = create_book(lib)
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
        create_author()

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
        book = create_book(lib)
        create_copy(book, 0)

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
        book = create_book(lib, is_best_seller=True)
        create_copy(book, 0)

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
        book = create_book(lib)
        create_copy(book, 0)
        create_copy(book, 1)

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
        book = create_book(lib)
        create_copy(book, 0)
        create_copy(book, 1)

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
        book = create_book(lib)
        create_copy(book, 0)
        create_copy(book, 1)

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
        book = create_book(lib)
        create_copy(book, 0)

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
        book = create_book(lib, is_best_seller=True)
        create_copy(book, 0)

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
        book_a = create_book(lib, title='A')
        create_copy(book_a, 0)
        book_b = create_book(lib, reference=True, title="B")
        create_copy(book_b, 0)

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


class TestCaseSettings:
    def first(self):
        library = create_library()
        librarian = create_user(Librarian, library, 1)

        b1 = librarian.create_b1(library)
        librarian.create_copy(b1, 3)
        b2 = librarian.create_b2(library)
        librarian.create_copy(b2, 2)
        b3 = librarian.create_b3(library)
        librarian.create_copy(b3, 1)

        av1 = librarian.create_av1(library)
        av2 = librarian.create_av2(library)

        p1 = librarian.create_p1(library)
        p2 = librarian.create_p2(library)
        p3 = librarian.create_p3(library)

    def second(self):
        library = create_library()
        librarian = create_user(Librarian, library, 1)

        b1 = librarian.create_b1(library)
        librarian.create_copy(b1, 3)
        b2 = librarian.create_b2(library)
        librarian.create_copy(b2, 2)
        b3 = librarian.create_b3(library)
        librarian.create_copy(b3, 1)

        av1 = librarian.create_av1(library)
        av2 = librarian.create_av2(library)

        p1 = librarian.create_p1(library)
        p2 = librarian.create_p2(library)
        p3 = librarian.create_p3(library)

        librarian.remove_copy(b1, 2)
        librarian.remove_copy(b3, 1)
        librarian.remove_patron(2)

    def bdclear(self):
        Patron.objects.filter().delete()
        AudioVideo.objects.filter().delete()
        Copy.objects.filter().delete()
        Book.objects.filter().delete()
        Library.objects.filter().delete()
        Librarian.objects.filter().delete()


class FirstTestCase(TestCase):
    def setUp(self):
        library = create_library()
        librarian = create_user(Librarian, library, 1)

    def testCase(self):
        print("Test 1")
        library = Library.objects.get(id=1)
        librarian = Librarian.objects.get(id=1)

        b1 = librarian.create_b1(library)
        librarian.create_copy(b1, 3)
        b2 = librarian.create_b2(library)
        librarian.create_copy(b2, 2)
        b3 = librarian.create_b3(library)
        librarian.create_copy(b3, 1)

        av1 = librarian.create_av1(library)
        av2 = librarian.create_av2(library)

        p1 = librarian.create_p1(library)
        p2 = librarian.create_p2(library)
        p3 = librarian.create_p3(library)

        print("The number of documents in the System is " + str(Document.objects.count()) +
              " and the number of users is " + str(User.objects.count()))

        TestCaseSettings.bdclear(self)


class SecondTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)

    def testCase(self):
        print("Test 2")
        librarian = Librarian.objects.get(id=1)
        b1 = Book.objects.get(id=1)
        b3 = Book.objects.get(id=3)

        librarian.remove_copy(b1, 2)
        librarian.remove_copy(b3, 1)
        librarian.remove_patron(2)

        print("The number of documents in the System is " + str(Document.objects.count()) +
              " and the number of users is " + str(User.objects.count()))

        TestCaseSettings.bdclear(self)


class ThirdTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)

    def testCase(self):
        print("Test 3")
        librarian = Librarian.objects.get(id=1)

        librarian.patron_information(1)
        librarian.patron_information(3)

        TestCaseSettings.bdclear(self)


class FourthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.second(self)

    def testCase(self):
        print("Test 4")
        librarian = Librarian.objects.get(id=1)
        librarian.patron_information(2)
        librarian.patron_information(3)

        TestCaseSettings.bdclear(self)


class FifthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.second(self)

    def testCase(self):
        print("Test 5")
        p2 = Patron.objects.get(first_name='Nadia')
        b1 = Book.objects.get(id=1)
        if p2.in_library():
            p2.check_out_doc(b1)
        else:
            print("p2 is not a patron of the library hence he cannot check out any document.")

        TestCaseSettings.bdclear(self)


class SixthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.second(self)

    def testCase(self):
        print("Test 6")
        librarian = Librarian.objects.get(id=1)
        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        p1 = Patron.objects.get(first_name='Sergey')
        p3 = Patron.objects.get(first_name='Elvira')
        p1.check_out_doc(b1)
        p3.check_out_doc(b1)
        p3.check_out_doc(b2)
        librarian.patron_information(1)
        librarian.patron_information(3)

        TestCaseSettings.bdclear(self)


class SeventhTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)

    def testCase(self):
        librarian = Librarian.objects.get(id=1)
        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        b3 = Book.objects.get(id=3)
        p1 = Patron.objects.get(first_name='Sergey')
        p2 = Patron.objects.get(first_name='Nadia')
        p3 = Patron.objects.get(first_name='Elvira')
        av1 = AudioVideo.objects.get(title="Null References: The Billion Dollar Mistake")
        av2 = AudioVideo.objects.get(title="Information Entropy")

        p1.check_out_doc(b1)
        p1.check_out_doc(b2)
        p1.check_out_doc(b3)
        p1.check_out_doc(av1)
        p2.check_out_doc(b1)
        p2.check_out_doc(b2)
        p2.check_out_doc(av2)
        librarian.patron_information(1)
        librarian.patron_information(2)

        TestCaseSettings.bdclear(self)


# class EighthTestCase(TestCase):
#     def setUp(self):
#         TestCaseSettings.first(self)
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
#         TestCaseSettings.bdclear(self)


class NinthTestCase(TestCase):
    def setUp(self):
        FirstTestCase.setUp(self)

    def testCase(self):
        FirstTestCase.testCase(self)