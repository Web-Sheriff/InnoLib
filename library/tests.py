# from django.core.exceptions import ObjectDoesNotExist
# from django.test import TestCase
#
# from library.models import *


# def create_library():
#     return Library.objects.create()
#
#
# def create_user(class_model, library, num):
#     user = class_model.objects.create(login='test', password='test', first_name='test', second_name='test',
#                                       address='test', phone_number='test', fine=0)
#     UserCard.objects.create(user=user, library_card_number=num, library=library)
#     return user
#
#
# def create_book(library, is_best_seller=False, reference=False, title='"Good_book"'):
#     class_model = ReferenceBook if reference else Book
#     return class_model.objects.create(library=library, title=title, price_value=0, is_best_seller=is_best_seller,
#                                       edition='0', publisher='test', year=2000)


''' p1 '''


# def create_p1(library):
#     user = Faculty.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso',
#                                   address="Via Margutta, 3", phone_number='30001')
#     UserCard.objects.create(user=user, library_card_number=1010, library=library)
#     return user
#
#
# ''' p2 '''
#
#
# def create_p2(library):
#     user = Student.objects.create(login='test', password='test', first_name='Nadia', second_name='Teixeira',
#                                   address="Via Sacra, 13", phone_number='30002')
#     UserCard.objects.create(user=user, library_card_number=1011, library=library)
#     return user
#
#
# ''' p3 '''
#
#
# def create_p3(library):
#     user = Student.objects.create(login='test', password='test', first_name='Elvira', second_name='Espindola',
#                                   address="Via del Corso, 22", phone_number='30003')
#     UserCard.objects.create(user=user, library_card_number=1100, library=library)
#     return user
#
#
# ''' s '''
#
#
# def create_s(library):
#     user = Student.objects.create(login='test', password='test', first_name='Andrey', second_name='Velo',
#                                   address="Avenida Mazatlan 250", phone_number='30004')
#     UserCard.objects.create(user=user, library_card_number=1101, library=library)
#     return user
#
#
# ''' v '''
#
#
# def create_v(library):
#     user = Student.objects.create(login='test', password='test', first_name='Veronika', second_name='Rama',
#                                   address="Stret Atocha, 27", phone_number='30005')
#     UserCard.objects.create(user=user, library_card_number=1110, library=library)
#     return user


# ''' d1 '''
#
#
# def create_d1(library):
#     return Book.objects.create(library=library, title="Introduction to Algorithms", price_value=0, is_best_seller=False,
#                                edition="Third edition", publisher='MIT Press', year=2009)
#
#
# ''' d2 '''
#
#
# def create_d2(library):
#     return Book.objects.create(library=library, title="Design Patterns: Elements of Reusable Object-Oriented Software",
#                                price_value=0, is_best_seller=True, edition="First edition",
#                                publisher="Addison-Wesley Professional", year=2003)
#
#
# ''' d3 '''
#
#
# def create_d3(library):
#     return ReferenceBook.objects.create(library=library, title="The Mythical Man-month", price_value=0,
#                                         is_best_seller=False, edition="Second edition",
#                                         publisher="Addison-Wesley Longman Publishing Co., Inc", year=1995)
#
#
# def create_copy(document, number):
#     Copy.objects.create(document=document, number=number)
#
#
# def create_author():
#     return Author.objects.create(name='Unnamed_author')
#
#
# def create_av(library, title="Test"):
#     return AudioVideo.objects.create(library=library, title=title, price_value=0)
#
#
# class TestCaseSettings:
#     def first(self):
#         library = create_library()
#         librarian = create_user(Librarian, library, 1)
#
#         d1 = librarian.create_d1(library)
#         librarian.create_copy(d1, 3)
#         d2 = librarian.create_b2(library)
#         librarian.create_copy(d2, 3)
#         d3 = librarian.create_b3(library)
#         librarian.create_copy(d3, 2)
#
#         p1 = librarian.create_p1(library)
#         p2 = librarian.create_p2(library)
#         p3 = librarian.create_p3(library)
#         s = librarian.create_s(library)
#         v = librarian.create_v(library)
#
#     def bdclear(self):
#         Patron.objects.filter().delete()
#         AudioVideo.objects.filter().delete()
#         Copy.objects.filter().delete()
#         Book.objects.filter().delete()
#         Library.objects.filter().delete()
#         Librarian.objects.filter().delete()
#
#
# class FirstTestCase(TestCase):
#     def setUp(self):
#         TCS = TestCaseSettings()
#         # TestCaseSettings.first(self)
#         TCS.first()
#
#     def testCase(self):
#         print("Test 1")
#         librarian = Librarian.objects.get(id=1)
#         d1 = Book.objects.get(id=1)
#         d2 = Book.objects.get(id=2)
#         try:
#             h = librarian.create_p1(d1.library)
#             p1 = Patron.objects.get(id=1)
#         except ObjectDoesNotExist:
#             print("p1 is not a patron of the library hence he cannot check out any document.")
#             return
#
#         p1.check_out_doc(d1)
#         p1.check_out_doc(d2)
#         date_checkout_d1 = datetime.date(2018,3,5)
#         date_chekcout_d2 = datetime.date(2018,3,5)
#         p1.return_doc(d1)
#         p1.return_doc(d2)
#         date_return_d1 = datetime.date(2018,4,2)
#         date_return_d2 = datetime.date(2018,4,2)
#
#         if (date_return_d1-date_checkout_d1 < d1.booking_period):
#             print("Overdue for the book "+d1.title+" is 0 days")
#             print("Fine for 0 days is 0 rub.")
#         else:
#             time = date_return_d1 - date_checkout_d1
#             print("Overdue for the book " + d1.title + " is "+str(time)+" days")
#             print("Fine for " + str(time) + " days is " + str(p1.fine))
#
#         TestCaseSettings.bdclear()
#
# ftc = FirstTestCase()
# ftc.setUp()
# ftc.testCase()
# ftc.tearDown()
#
#
# FirstTestCase.setUp()
# FirstTestCase.testCase()
# FirstTestCase.tearDown()


from django.test import TestCase
from library.models import *


class DocumentTestCase(TestCase):
    document_one = None
    document_two = None
    patron_one = None

    def setUp(self):
        self.library = Library.objects.create()
        self.document_one = Document.objects.create(library=self.library, title="Introduction to Algorithms", price_value=0, is_best_seller=False, edition="Third edition", publisher='MIT Press', year=2009)
        self.document_two = Document.objects.create(library=self.library, title="Design Patterns: Elements of Reusable Object-Oriented Software", price_value=0, is_best_seller=True, edition="First edition", publisher="Addison-Wesley Professional", year=2003)
        self.patron_one = Patron.objects.create(login='test', password='test', first_name='Sergey', second_name='Afonso', address="Via Margutta, 3", phone_number='30001', fine=0)
        UserCard.objects.create(user=self.patron_one, library_card_number=1010, library=self.library)
        self.patron_one.check_out_doc(document=self.document_one)
        self.patron_one.check_out_doc(document=self.document_two)

    def test_patron_has_no_overdue_and_fine(self):
        self.patron_one.return_doc(document=self.document_two)

        date_checkout_d1 = datetime.date(2018,3,5)
        date_chekcout_d2 = datetime.date(2018,3,5)
        date_return_d1 = datetime.date(2018,4,2)
        date_return_d2 = datetime.date(2018,4,2)

        if date_return_d1 - date_checkout_d1 < datetime.timedelta(weeks=2):
            print("Overdue for the book "+self.document_one.title+" is 0 days")
            print("Fine for 0 days is 0 rub.")
        else:
            time = date_return_d1 - date_checkout_d1
            print("Overdue for the book " + self.document_one.title + " is "+str(time)+" days")
            print("Fine for " + str(time) + " days is " + str(self.patron_one.fine))



    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')