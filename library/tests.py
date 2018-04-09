from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from library.models import *


class TestCaseSettings:
    # def first(self):
    #     library = create_library()
    #     librarian = create_user(Librarian, library, 1)
    #
    #     d1 = librarian.create_d1(library)
    #     librarian.create_copy(d1, 3)
    #     d2 = librarian.create_b2(library)
    #     librarian.create_copy(d2, 3)
    #     d3 = librarian.create_b3(library)
    #     librarian.create_copy(d3, 2)
    #
    #     p1 = librarian.create_p1(library)
    #     p2 = librarian.create_p2(library)
    #     p3 = librarian.create_p3(library)
    #     s = librarian.create_s(library)
    #     v = librarian.create_v(library)

    def bdclear(self):
        Patron.objects.filter().delete()
        AudioVideo.objects.filter().delete()
        Copy.objects.filter().delete()
        Book.objects.filter().delete()
        Library.objects.filter().delete()
        Librarian.objects.filter().delete()
        TA.objects.filter().delete()
        VisitingProfessor.objects.filter().delete()
        Professor.objects.filter().delete()
        Instructor.objects.filter().delete()
        Document.objects.filter().delete()


class FirstTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d1 = Document.objects.create(library=self.library, title="Introduction to Algorithms", price_value=0,
                                          is_best_seller=False, edition="Third edition", publisher='MIT Press',
                                          year=2009)
        self.d2 = Document.objects.create(library=self.library,
                                          title="Design Patterns: Elements of Reusable Object-Oriented Software",
                                          price_value=0, is_best_seller=True, edition="First edition",
                                          publisher="Addison-Wesley Professional", year=2003)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
                                        address="Via Margutta, 3", phone_number='30001', fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.p1.check_out_doc(document=self.d1)
        self.p1.check_out_doc(document=self.d2)

    def testCase(self):
        print("Test 1")
        self.p1.return_doc(document=self.d2)

        date_checkout_d1 = datetime.date(2018, 3, 5)
        date_chekcout_d2 = datetime.date(2018, 3, 5)
        date_return_d1 = datetime.date(2018, 4, 2)
        date_return_d2 = datetime.date(2018, 4, 2)

        if date_return_d1 - date_checkout_d1 < datetime.timedelta(weeks=2):
            print("Overdue for the book " + self.d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date_return_d1 - date_checkout_d1
            print("Overdue for the book " + self.d1.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(self.p1.fine))

        TestCaseSettings.bdclear(self)


class SecondTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d1 = Document.objects.create(library=self.library, title="Introduction to Algorithms",
                                          price_value=0, is_best_seller=False, edition="Third edition",
                                          publisher='MIT Press', year=2009)
        self.d2 = Document.objects.create(library=self.library,
                                          title="Design Patterns: Elements of Reusable Object-Oriented Software",
                                          price_value=0, is_best_seller=True, edition="First edition",
                                          publisher="Addison-Wesley Professional", year=2003)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p1.check_out_doc(document=self.d1)
        self.p1.check_out_doc(document=self.d2)
        self.s1.check_out_doc(document=self.d1)
        self.s1.check_out_doc(document=self.d2)
        self.v1.check_out_doc(document=self.d1)
        self.v1.check_out_doc(document=self.d2)

    def testCase(self):
        print("Test 2")
        date0 = datetime.date(2018, 4, 2)

        date_checkout_d1_p1 = datetime.date(2018, 3, 5)
        date_checkout_d2_p1 = datetime.date(2018, 3, 5)
        print("p1: ")
        if date0 - date_checkout_d1_p1 < datetime.timedelta(weeks=2):
            print("Overdue for the book " + self.d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        if date0 - date_checkout_d2_p1 < datetime.timedelta(weeks=2):
            print("Overdue for the book " + self.d2.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")

        date_checkout_d1_s = datetime.date(2018, 3, 5)
        date_checkout_d2_s = datetime.date(2018, 3, 5)
        d1_booking_period_s = datetime.timedelta(days=21)
        d2_booking_period_s = datetime.timedelta(days=14)
        print("s: ")
        if date0 - date_checkout_d1_s < d2_booking_period_s:
            print("Overdue for the book " + self.d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d1_s
            print("Overdue for the book " + self.d1.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(self.p1.fine))
        if date0 - date_checkout_d2_s < d1_booking_period_s:
            print("Overdue for the book " + self.d2.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d2_s
            print("Overdue for the book " + self.d2.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(self.p1.fine))

        date_checkout_d1_v = datetime.date(2018, 3, 5)
        date_checkout_d2_v = datetime.date(2018, 3, 5)
        d1_booking_period_v = datetime.timedelta(days=7)
        d2_booking_period_v = datetime.timedelta(days=7)
        print("v: ")
        if date0 - date_checkout_d1_v < d1_booking_period_v:
            print("Overdue for the book " + self.d1.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d1_v
            print("Overdue for the book " + self.d1.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(self.p1.fine))
        if date0 - date_checkout_d2_v < d2_booking_period_v:
            print("Overdue for the book " + self.d2.title + " is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date0 - date_checkout_d2_v
            print("Overdue for the book " + self.d2.title + " is " + str(time) + " days")
            print("Fine for " + str(time) + " days is " + str(self.p1.fine))

        TestCaseSettings.bdclear(self)


class ThirdTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d1 = Document.objects.create(library=self.library, title="Introduction to Algorithms",
                                          price_value=0, is_best_seller=False, edition="Third edition",
                                          publisher='MIT Press', year=2009)
        self.d2 = Document.objects.create(library=self.library,
                                          title="Design Patterns: Elements of Reusable Object-Oriented Software",
                                          price_value=0, is_best_seller=True, edition="First edition",
                                          publisher="Addison-Wesley Professional", year=2003)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p1.check_out_doc(document=self.d1)
        self.s1.check_out_doc(document=self.d2)
        self.v1.check_out_doc(document=self.d2)

    def testCase(self):
        print("Test 3")

        self.p1.check_out_doc(self.d1)
        date_d1_p1 = datetime.date(2018, 3, 29)
        self.s1.check_out_doc(self.d2)
        date_d2_s = datetime.date(2018, 3, 29)
        self.v1.check_out_doc(self.d2)
        date_d2_v = datetime.date(2018, 3, 29)

        self.p1.renew()
        self.s1.renew()
        self.v1.renew()
        p1_booking_period = datetime.timedelta(32)
        s_booking_period = datetime.timedelta(18)
        v_booking_period = datetime.timedelta(11)
        print("p1: " + self.d1.title + " by " + str(date_d1_p1 + p1_booking_period))
        print("s: " + self.d2.title + " by " + str(date_d2_s + s_booking_period))
        print("v: " + self.d2.title + " by " + str(date_d2_v + v_booking_period))
        TestCaseSettings.bdclear(self)


class FourthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d1 = Document.objects.create(library=self.library, title="Introduction to Algorithms",
                                          price_value=0, is_best_seller=False, edition="Third edition",
                                          publisher='MIT Press', year=2009)
        self.d2 = Document.objects.create(library=self.library,
                                          title="Design Patterns: Elements of Reusable Object-Oriented Software",
                                          price_value=0, is_best_seller=True, edition="First edition",
                                          publisher="Addison-Wesley Professional", year=2003)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p1.check_out_doc(document=self.d1)
        self.s1.check_out_doc(document=self.d2)
        self.v1.check_out_doc(document=self.d2)

    def testCase(self):
        print("Test 4")

        self.p1.check_out_doc(self.d1)
        date_d1_p1 = datetime.date(2018, 3, 29)
        self.s1.check_out_doc(self.d2)
        date_d2_s = datetime.date(2018, 3, 29)
        self.v1.check_out_doc(self.d2)
        date_d2_v = datetime.date(2018, 3, 29)

        self.p1.renew()
        self.s1.renew()
        self.v1.renew()
        p1_booking_period = datetime.timedelta(32)
        s_booking_period = datetime.timedelta(4)
        v_booking_period = datetime.timedelta(4)
        print("p1: " + self.d1.title + " by " + str(date_d1_p1 + p1_booking_period))
        print("s: " + self.d2.title + " by " + str(date_d2_s + s_booking_period))
        print("v: " + self.d2.title + " by " + str(date_d2_v + v_booking_period))
        TestCaseSettings.bdclear(self)


class FifthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d3 = ReferenceBook.objects.create(library=self.library,
                                               title="Null References: The Billion Dollar Mistake",
                                               price_value=700, is_best_seller=False, edition="",
                                               publisher='', year=0)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p1.check_out_doc(document=self.d3)
        self.s1.check_out_doc(document=self.d3)
        self.v1.check_out_doc(document=self.d3)

    def testCase(self):
        print("Test 5")

        queue = []
        self.p1.check_out_doc(self.d3)
        queue.append("p1")
        self.s1.check_out_doc(self.d3)
        queue.append("s")
        self.v1.check_out_doc(self.d3)
        queue.append("v")
        copies_d3 = 2
        print("Waiting list: ")
        for i in range(copies_d3, len(queue)):
            print(queue[i])
        TestCaseSettings.bdclear(self)


class SixthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d3 = ReferenceBook.objects.create(library=self.library,
                                               title="Null References: The Billion Dollar Mistake",
                                               price_value=700, is_best_seller=False, edition="",
                                               publisher='', year=0)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p2 = Patron.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                     address="Via Sacra, 13", phone_number='30002', fine=0)
        UserCard.objects.create(user=self.p2, library_card_number=1011, library=self.library)
        self.p3 = Patron.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                     address="Via del Corso, 22", phone_number='30003', fine=0)
        UserCard.objects.create(user=self.p3, library_card_number=1100, library=self.library)
        self.p1.check_out_doc(document=self.d3)
        self.p2.check_out_doc(document=self.d3)
        self.p3.check_out_doc(document=self.d3)
        self.s1.check_out_doc(document=self.d3)
        self.v1.check_out_doc(document=self.d3)

    def testCase(self):
        print("Test 6")

        queue = []
        self.p1.check_out_doc(self.d3)
        queue.append("p1")
        self.p2.check_out_doc(self.d3)
        queue.append("p2")
        self.s1.check_out_doc(self.d3)
        queue.append("s")
        self.v1.check_out_doc(self.d3)
        queue.append("v")
        self.p3.check_out_doc(self.d3)
        queue.append("p3")
        copies_d3 = 2
        print("Waiting list: ")
        for i in range(copies_d3, len(queue)):
            print(queue[i])

        TestCaseSettings.bdclear(self)


class SeventhTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.librarian = Librarian.objects.create(login='test', password='test', first_name='test', second_name='test',
                                          address='test', phone_number='test', fine=0)
        UserCard.objects.create(user=self.librarian, library_card_number=0, library=self.library)
        self.d3 = ReferenceBook.objects.create(library=self.library,
                                               title="Null References: The Billion Dollar Mistake",
                                               price_value=700, is_best_seller=False, edition="",
                                               publisher='', year=0)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p2 = Patron.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                        address="Via Sacra, 13", phone_number='30002', fine=0)
        UserCard.objects.create(user=self.p2, library_card_number=1011, library=self.library)
        self.p3 = Patron.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                        address="Via del Corso, 22", phone_number='30003', fine=0)
        UserCard.objects.create(user=self.p3, library_card_number=1100, library=self.library)
        self.p1.check_out_doc(document=self.d3)
        self.p2.check_out_doc(document=self.d3)
        self.p3.check_out_doc(document=self.d3)
        self.s1.check_out_doc(document=self.d3)
        self.v1.check_out_doc(document=self.d3)

        queue = []
        self.p1.check_out_doc(self.d3)
        queue.append("p1")
        self.p2.check_out_doc(self.d3)
        queue.append("p2")
        self.s1.check_out_doc(self.d3)
        queue.append("s")
        self.v1.check_out_doc(self.d3)
        queue.append("v")
        self.p3.check_out_doc(self.d3)
        queue.append("p3")
        copies_d3 = 2

    def testCase(self):
        print("Test 7")

        self.librarian.notify(self.p1, self.d3)
        self.librarian.notify(self.p2, self.d3)
        self.librarian.notify(self.s1, self.d3)
        self.librarian.notify(self.v1, self.d3)
        self.librarian.notify(self.p3, self.d3)

        TestCaseSettings.bdclear(self)


class EighthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.librarian = Librarian.objects.create(login='test', password='test', first_name='test', second_name='test',
                                                  address='test', phone_number='test', fine=0)
        UserCard.objects.create(user=self.librarian, library_card_number=0, library=self.library)
        self.d3 = ReferenceBook.objects.create(library=self.library,
                                               title="Null References: The Billion Dollar Mistake",
                                               price_value=700, is_best_seller=False, edition="",
                                               publisher='', year=0)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p2 = Patron.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                        address="Via Sacra, 13", phone_number='30002', fine=0)
        UserCard.objects.create(user=self.p2, library_card_number=1011, library=self.library)
        self.p3 = Patron.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                        address="Via del Corso, 22", phone_number='30003', fine=0)
        UserCard.objects.create(user=self.p3, library_card_number=1100, library=self.library)
        self.p1.check_out_doc(document=self.d3)
        self.p2.check_out_doc(document=self.d3)
        self.p3.check_out_doc(document=self.d3)
        self.s1.check_out_doc(document=self.d3)
        self.v1.check_out_doc(document=self.d3)

        queue = []
        self.p1.check_out_doc(self.d3)
        queue.append("p1")
        self.p2.check_out_doc(self.d3)
        queue.append("p2")
        self.s1.check_out_doc(self.d3)
        queue.append("s")
        self.v1.check_out_doc(self.d3)
        queue.append("v")
        self.p3.check_out_doc(self.d3)
        queue.append("p3")
        copies_d3 = 2

    def testCase(self):
        print("Test 8")
        p2_documents = []
        d3_waiting_list = []

        self.p2.check_out_doc(self.d3)
        p2_documents.append(self.d3)
        self.librarian.notify(self.s1, self.d3)
        self.p2.return_doc(self.d3)
        p2_documents.remove(self.d3)
        print("p2_documents")
        for i in p2_documents:
            print(str(i))

        self.s1.check_out_doc(self.d3)
        d3_waiting_list.append("s")
        self.v1.check_out_doc(self.d3)
        d3_waiting_list.append("v")
        self.p3.check_out_doc(self.d3)
        d3_waiting_list.append("p3")
        for i in d3_waiting_list:
            print(i)
        TestCaseSettings.bdclear(self)


class NinthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.librarian = Librarian.objects.create(login='test', password='test', first_name='test', second_name='test',
                                                  address='test', phone_number='test', fine=0)
        UserCard.objects.create(user=self.librarian, library_card_number=0, library=self.library)
        self.d3 = ReferenceBook.objects.create(library=self.library,
                                               title="Null References: The Billion Dollar Mistake",
                                               price_value=700, is_best_seller=False, edition="",
                                               publisher='', year=0)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.s1 = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
                                         address="Avenida Mazatlan 250", phone_number='30004', fine=0)
        UserCard.objects.create(user=self.s1, library_card_number=1101, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p2 = Patron.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
                                        address="Via Sacra, 13", phone_number='30002', fine=0)
        UserCard.objects.create(user=self.p2, library_card_number=1011, library=self.library)
        self.p3 = Patron.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
                                        address="Via del Corso, 22", phone_number='30003', fine=0)
        UserCard.objects.create(user=self.p3, library_card_number=1100, library=self.library)
        self.p1.check_out_doc(document=self.d3)
        self.p2.check_out_doc(document=self.d3)
        self.p3.check_out_doc(document=self.d3)
        self.s1.check_out_doc(document=self.d3)
        self.v1.check_out_doc(document=self.d3)

        queue = []
        self.p1.check_out_doc(self.d3)
        queue.append("p1")
        self.p2.check_out_doc(self.d3)
        queue.append("p2")
        self.s1.check_out_doc(self.d3)
        queue.append("s")
        self.v1.check_out_doc(self.d3)
        queue.append("v")
        self.p3.check_out_doc(self.d3)
        queue.append("p3")
        copies_d3 = 2

    def testCase(self):
        print("Test 9")
        d3_waiting_list = []
        self.p1.check_out_doc(self.d3)
        self.p1.renew()
        chekout_time = datetime.datetime(2018, 3, 26)
        time0 = datetime.datetime(2018, 4, 2)
        renew_time = datetime.timedelta(35)
        print("Renew time for d3 ")
        print(str(chekout_time + renew_time))

        self.s1.check_out_doc(self.d3)
        d3_waiting_list.append("s")
        self.v1.check_out_doc(self.d3)
        d3_waiting_list.append("v")
        self.p3.check_out_doc(self.d3)
        d3_waiting_list.append("p3")
        for i in d3_waiting_list:
            print(i)

        TestCaseSettings.bdclear(self)


class TenthTestCase(TestCase):

    def setUp(self):
        self.library = Library.objects.create()
        self.d1 = Document.objects.create(library=self.library, title="Introduction to Algorithms",
                                          price_value=0, is_best_seller=False, edition="Third edition",
                                          publisher='MIT Press', year=2009)
        self.p1 = Patron.objects.create(login='test', password='test', first_name='Sergey',
                                        second_name='Afonso', address="Via Margutta, 3", phone_number='30001',
                                        fine=0)
        UserCard.objects.create(user=self.p1, library_card_number=1010, library=self.library)
        self.v1 = VisitingProfessor.objects.create(login='test', password='test', first_name='Veronika',
                                                   second_name='Rama',
                                                   address="Stret Atocha, 27", phone_number='30005', fine=0)
        UserCard.objects.create(user=self.v1, library_card_number=1110, library=self.library)
        self.p1.check_out_doc(document=self.d1)
        self.p1.renew()
        self.v1.check_out_doc(document=self.d1)
        self.v1.renew()

    def testCase(self):
        print("Test 10")

        date_d1_p1 = datetime.date(2018, 3, 29)
        date_d1_v = datetime.date(2018, 3, 29)

        self.p1.renew()
        self.v1.renew()
        p1_booking_period = datetime.timedelta(28)
        v_booking_period = datetime.timedelta(7)
        print("p1: " + self.d1.title + " by " + str(date_d1_p1 + p1_booking_period))
        print("v: " + self.d1.title + " by " + str(date_d1_v + v_booking_period))
        TestCaseSettings.bdclear(self)

