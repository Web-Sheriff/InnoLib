import datetime

from django.test import TestCase
from library.models import *
from django.core.exceptions import ObjectDoesNotExist


def create_library():
    return Library.objects.create()


def create_user(class_model, library, num):
    user = class_model.objects.create(login='test', password='test', first_name='test', second_name='test',
                                      address='test', phone_number='test')
    UserCard.objects.create(user=user, library_card_number=num, library=library)
    return user



def create_book(library, is_best_seller=False, reference=False, title='"Good_book"'):
    class_model = ReferenceBook if reference else Book
    return class_model.objects.create(library=library, title=title, price_value=0, is_best_seller=is_best_seller,
                                      edition='0', publisher='test', year=2000)

''' p1 '''
def create_p1(library):
    user = Faculty.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
                                  address="Via Margutta, 3", phone_number='30001')
    UserCard.objects.create(user=user, library_card_number=1010, library=library)
    return user

''' p2 '''
def create_p2(library):
    user = Student.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                  address="Via Sacra, 13", phone_number='30002')
    UserCard.objects.create(user=user, library_card_number=1011, library=library)
    return user

''' p3 '''
def create_p3(library):
    user = Student.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                  address="Via del Corso, 22", phone_number='30003')
    UserCard.objects.create(user=user, library_card_number=1100, library=library)
    return user

''' b1 '''
def create_b1(library):
    return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0, is_best_seller=False,
                                      edition="Third edition", publisher='MIT Press', year=2009)

''' b2 '''
def create_b2(library):
    return Book.objects.create(library=library, title="Design Patterns: Elements of Reusable Object-Oriented Software",
                               price_value=0, is_best_seller=True, edition="First edition",
                               publisher="Addison-Wesley Professional", year=2003)

''' b3 '''
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





class TestCaseSettings:
    def first(self):
        library = create_library()
        librarian = create_user(Librarian, library, 1)

        b1 = librarian.create_b1(library)
        librarian.create_copy(b1, 3)
        b2 = librarian.create_b2(library)
        librarian.create_copy(b2, 3)
        b3 = librarian.create_b3(library)
        librarian.create_copy(b3, 2)

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

        copy_count = 0
        for copy in Copy.objects.filter():
            copy_count += copy.number

        print("The number of documents in the System is " + str(copy_count + AudioVideo.objects.count()) +
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

        copy_count = 0
        for copy in Copy.objects.filter():
            copy_count += copy.number

        print("The number of documents in the System is " + str(copy_count + AudioVideo.objects.count()) +
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
        try:
            p2 = Patron.objects.get(id=3)
        except ObjectDoesNotExist:
            print("p2 is not a patron of the library hence he cannot check out any document.")
            return
        b1 = Book.objects.get(id=1)
        p2.check_out_doc(b1)

        TestCaseSettings.bdclear(self)


class SixthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.second(self)

    def testCase(self):
        print("Test 6")
        librarian = Librarian.objects.get(id=1)
        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)

        p1 = Patron.objects.get(id=2)
        p3 = Patron.objects.get(id=4)
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
        print("Test 7")
        librarian = Librarian.objects.get(id=1)
        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        b3 = Book.objects.get(id=3)
        p1 = Patron.objects.get(id=2)
        p2 = Patron.objects.get(id=3)
        p3 = Patron.objects.get(id=4)
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
#         print("Test 8")
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
        print("Test 9")
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

        copy_count = 0
        for copy in Copy.objects.filter():
            copy_count += copy.number

        print("The number of documents in the System is " + str(copy_count + AudioVideo.objects.count()) +
              " and the number of users is " + str(User.objects.count()))
