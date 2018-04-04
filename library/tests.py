from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from library.models import *


def create_library():
    return Library.objects.create()


def create_user(class_model, library, num):
    user = class_model.objects.create(login='test', password='test', first_name='test', second_name='test',address='test', phone_number='test')
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


''' s '''


def create_s(library):
    user = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                  address="Avenida Mazatlan 250", phone_number='30004')
    UserCard.objects.create(user=user, library_card_number=1101, library=library)
    return user


''' v '''


def create_v(library):
    user = Student.objects.create(login='test', password='test', first_name='Veronika', second_name='Rama',
                                  address="Stret Atocha, 27", phone_number='30005')
    UserCard.objects.create(user=user, library_card_number=1110, library=library)
    return user


''' d1 '''


def create_d1(library):
    return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0, is_best_seller=False,
                               edition="Third edition", publisher='MIT Press', year=2009)


''' d2 '''


def create_d2(library):
    return Book.objects.create(library=library, title="Design Patterns: Elements of Reusable Object-Oriented Software",
                               price_value=0, is_best_seller=True, edition="First edition",
                               publisher="Addison-Wesley Professional", year=2003)


''' d3 '''


def create_d3(library):
    return ReferenceBook.objects.create(library=library, title="The Mythical Man-month", price_value=0,
                                        is_best_seller=False, edition="Second edition",
                                        publisher="Addison-Wesley Longman Publishing Co., Inc", year=1995)


def create_copy(document, number):
    Copy.objects.create(document=document, number=number)


def create_author():
    return Author.objects.create(name='Unnamed_author')


def create_av(library, title="Test"):
    return AudioVideo.objects.create(library=library, title=title, price_value=0)


class TestCaseSettings:
    def first(self):
        library = create_library()
        librarian = create_user(Librarian, library, 1)

        d1 = librarian.create_d1(library)
        librarian.create_copy(d1, 3)
        d2 = librarian.create_b2(library)
        librarian.create_copy(d2, 3)
        d3 = librarian.create_b3(library)
        librarian.create_copy(d3, 2)


        p1 = librarian.create_p1(library)
        p2 = librarian.create_p2(library)
        p3 = librarian.create_p3(library)
        s = librarian.create_s(library)
        v = librarian.create_v(library)

    def bdclear(self):
        Patron.objects.filter().delete()
        AudioVideo.objects.filter().delete()
        Copy.objects.filter().delete()
        Book.objects.filter().delete()
        Library.objects.filter().delete()
        Librarian.objects.filter().delete()


class FirstTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)

    def testCase(self):
        print("Test 1")
        librarian = Librarian.objects.get(id=1)
        d1 = Book.objects.get(id=1)
        d2 = Book.objects.get(id=2)
        p1 = Patron.objects.get(id=1)

        p1.check_out_doc(d1)
        p1.check_out_doc(d2)
        date_checkout_d1 = datetime.date(2018,3,5)
        date_chekcout_d2 = datetime.date(2018,3,5)
        p1.return_doc(d1)
        p1.return_doc(d2)
        date_return_d1 = datetime.date(2018,4,2)
        date_return_d2 = datetime.date(2018,4,2)

        if (date_return_d1-date_checkout_d1 < d1.booking_period):
            print("Overdue for the book "+d1.title+" is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date_return_d1 - date_checkout_d1
            print("Overdue for the book " + d1.title + " is "+str(time)+" days")
            print("Fine for "+ str(time)+ " days is " + str(p1.fine))

        TestCaseSettings.bdclear(self)


class SecondTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)

    def testCase(self):
        print("Test 2")
        librarian = Librarian.objects.get(id=1)
        d1 = Book.objects.get(id=1)
        d2 = Book.objects.get(id=2)
        p1 = Patron.objects.get(id=1)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)
        date0 = datetime.date(2018,4,2)

        p1.check_out_doc(d1)
        p1.check_out_doc(d2)
        date_checkout_d1_p1 = datetime.date(2018, 3, 5)
        date_checkout_d2_p1 = datetime.date(2018, 3, 5)
        print("p1: ")
        if (date0-date_checkout_d1_p1 < d1.booking_period):
            print("Overdue for the book "+d1.title+" is 0 days")
            print("Fine for 0 days is 0 rub.")
        if (date0-date_checkout_d2_p1 < d2.booking_period):
            print("Overdue for the book "+d2.title+" is 0 days")
            print("Fine for 0 days is 0 rub.")

        s.check_out_doc(d1)
        s.check_out_doc(d2)
        date_checkout_d1_s = datetime.date(2018, 3, 5)
        date_checkout_d2_s = datetime.date(2018, 3, 5)
        d1_booking_period_s = datetime.timedelta(days = 21)
        d2_booking_period_s = datetime.timedelta(days=14)
        print("s: ")
        if (date0 - date_checkout_d1_s < d1_booking_period_s):
            print("Overdue for the book " + d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d1_s
            print("Overdue for the book " + d1.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(p1.fine))
        if (date0 - date_checkout_d2_s < d2_booking_period_s):
            print("Overdue for the book " + d2.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d2_s
            print("Overdue for the book " + d2.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(p1.fine))

        v.check_out_doc(d1)
        v.check_out_doc(d2)
        date_checkout_d1_v = datetime.date(2018, 3, 5)
        date_checkout_d2_v = datetime.date(2018, 3, 5)
        d1_booking_period_v = datetime.timedelta(days=7)
        d2_booking_period_v = datetime.timedelta(days=7)
        print("v: ")
        if (date0 - date_checkout_d1_v < d1_booking_period_v):
            print("Overdue for the book " + d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d1_v
            print("Overdue for the book " + d1.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(p1.fine))
        if (date0 - date_checkout_d2_v < d2_booking_period_v):
            print("Overdue for the book " + d2.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d2_v
            print("Overdue for the book " + d2.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(p1.fine))

        TestCaseSettings.bdclear(self)


class ThirdTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 3")
        librarian = Librarian.objects.get(id=1)
        d1 = Book.objects.get(id=1)
        d2 = Book.objects.get(id=2)
        p1 = Patron.objects.get(id=1)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)

        p1.check_out_doc(d1)
        date_d1_p1 = datetime.date(2018,3,29)
        s.check_out_doc(d2)
        date_d2_s = datetime.date(2018, 3, 29)
        v.check_out_doc(d2)
        date_d2_v = datetime.date(2018, 3, 29)

        p1.renew()
        s.renew()
        v.renew()
        p1_booking_period = datetime.timedelta(32)
        s_booking_period = datetime.timedelta(18)
        v_booking_period = datetime.timedelta(11)
        print("p1: "+ d1.title + " by " + str(date_d1_p1+p1_booking_period))
        print("s: " + d2.title + " by " + str(date_d2_s + s_booking_period))
        print("v: " + d2.title + " by " + str(date_d2_v + v_booking_period))
        TestCaseSettings.bdclear(self)


class FourthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 4")
        librarian = Librarian.objects.get(id=1)
        d1 = Book.objects.get(id=1)
        d2 = Book.objects.get(id=2)
        p1 = Patron.objects.get(id=1)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)

        p1.check_out_doc(d1)
        date_d1_p1 = datetime.date(2018, 3, 29)
        s.check_out_doc(d2)
        date_d2_s = datetime.date(2018, 3, 29)
        v.check_out_doc(d2)
        date_d2_v = datetime.date(2018, 3, 29)

        p1.renew()
        s.renew()
        v.renew()
        p1_booking_period = datetime.timedelta(32)
        s_booking_period = datetime.timedelta(4)
        v_booking_period = datetime.timedelta(4)
        print("p1: " + d1.title + " by " + str(date_d1_p1 + p1_booking_period))
        print("s: " + d2.title + " by " + str(date_d2_s + s_booking_period))
        print("v: " + d2.title + " by " + str(date_d2_v + v_booking_period))
        TestCaseSettings.bdclear(self)
        TestCaseSettings.bdclear(self)


class FifthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 5")
        librarian = Librarian.objects.get(id=1)
        d3 = Book.objects.get(id=3)
        p1 = Patron.objects.get(id=1)
        p2 = Patron.objects.get(id=2)
        p3 = Patron.objects.get(id=3)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)

        queue = []
        p1.check_out_doc(d3)
        queue.append("p1")
        s.check_out_doc(d3)
        queue.append("s")
        v.check_out_doc(d3)
        queue.append("v")
        copies_d3 = 2
        print("Waiting list: ")
        for i in range (copies_d3,len(queue)):
            print(queue[i])
        TestCaseSettings.bdclear(self)


class SixthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 6")
        librarian = Librarian.objects.get(id=1)
        d3 = Book.objects.get(id=3)
        p1 = Patron.objects.get(id=1)
        p2 = Patron.objects.get(id=2)
        p3 = Patron.objects.get(id=3)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)

        queue = []
        p1.check_out_doc(d3)
        queue.append("p1")
        p2.check_out_doc(d3)
        queue.append("p2")
        s.check_out_doc(d3)
        queue.append("s")
        v.check_out_doc(d3)
        queue.append("v")
        p3.check_out_doc(d3)
        queue.append("p3")
        copies_d3 = 2
        print("Waiting list: ")
        for i in range(copies_d3, len(queue)):
            print(queue[i])

        TestCaseSettings.bdclear(self)


class SeventhTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 7")
        librarian = Librarian.objects.get(id=1)
        d3 = Book.objects.get(id = 3)
        p1 = Patron.objects.get(id=1)
        p2 = Patron.objects.get(id=2)
        p3 = Patron.objects.get(id=3)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)

        librarian.notify(p1,d3)
        librarian.notify(p2,d3)
        librarian.notify(s, d3)
        librarian.notify(v, d3)
        librarian.notify(p3, d3)

        TestCaseSettings.bdclear(self)


class EighthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 8")
        p2 = Patron.objects.get(id = 2)
        p2_documents = []
        d3_waiting_list = []
        librarian = Librarian.objects.get(id=1)
        s = Patron.objects.get(id=4)
        v = Patron.objects.get(id=5)
        p3 = Patron.objects.get(id=3)
        d3 = Book.objects.get(id = 3)

        p2.check_out_doc(d3)
        p2_documents.append(d3)
        librarian.notify(s,d3)
        p2.return_doc(d3)
        p2_documents.remove(d3)
        print("p2_documents")
        for i in p2_documents:
            print(str(i))

        s.check_out_doc(d3)
        d3_waiting_list.append("s")
        v.check_out_doc(d3)
        d3_waiting_list.append("v")
        p3.check_out_doc(d3)
        d3_waiting_list.append("p3")
        for i in d3_waiting_list:
            print(i)
        TestCaseSettings.bdclear(self)


class NinthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 9")
        d3_waiting_list = []
        d3 = Document.objects.get(id=3)
        p1 = Patron.objects.get(id=1)
        s = Patron.objects.get(id = 4)
        v = Patron.objects.get(id = 5)
        p3 = Patron.objects.get(id=3)
        p1.check_out_doc(d3)
        p1.renew()
        chekout_time = datetime.datetime(2018,3,26)
        time0 = datetime.datetime(2018,4,2)
        renew_time = datetime.timedelta(35)
        print("Renew time for d3 ")
        print(str(chekout_time+renew_time))

        s.check_out_doc(d3)
        d3_waiting_list.append("s")
        v.check_out_doc(d3)
        d3_waiting_list.append("v")
        p3.check_out_doc(d3)
        d3_waiting_list.append("p3")
        for i in d3_waiting_list:
            print(i)

        TestCaseSettings.bdclear(self)

    
class TenthTestCase(TestCase):
    def setUp(self):
        TestCaseSettings.first(self)
    def testCase(self):
        print("Test 10")
        librarian = Librarian.objects.get(id=1)
        p1 = Patron.objects.get(id=1)
        v = Patron.objects.get(id=5)
        d1 = Book.objects.get(id=1)

        p1.check_out_doc(d1)
        date_d1_p1 = datetime.date(2018, 3, 29)
        v.check_out_doc(d1)
        date_d1_v = datetime.date(2018, 3, 29)

        p1.renew()
        v.renew()
        p1_booking_period = datetime.timedelta(28)
        v_booking_period = datetime.timedelta(7)
        print("p1: " + d1.title + " by " + str(date_d1_p1 + p1_booking_period))
        print("v: " + d1.title + " by " + str(date_d1_v + v_booking_period))
        TestCaseSettings.bdclear(self)
        TestCaseSettings.bdclear(self)




'''
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
'''