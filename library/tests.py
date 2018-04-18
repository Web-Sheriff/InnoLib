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

    # def bdclear(self):
    #     Patron.objects.filter().delete()
    #     AudioVideo.objects.filter().delete()
    #     Copy.objects.filter().delete()
    #     Book.objects.filter().delete()
    #     Library.objects.filter().delete()
    #     Librarian.objects.filter().delete()
    #     TA.objects.filter().delete()
    #     VisitingProfessor.objects.filter().delete()
    #     Professor.objects.filter().delete()
    #     Instructor.objects.filter().delete()
    #     Document.objects.filter().delete()
    pass


class TestCase(TestCase):
    library = Library.objects.create()
    librarian = Librarian.objects.create(login='librarian', password='12345', mail='test@gmail.com', first_name='Librarian', second_name='Librairain', address='Inno', phone_number='1235435')
    user = librarian.create_user(class_model=Student, library=library, num=10)
    bORUTO = Book.objects.create(library=library, title='NARUTO', price_value='50', is_best_seller=False, edition='4th', publisher='ddd', year='1999')
    c = Copy.objects.create(document=bORUTO, number=2)
    user.user_card.copies.add(c)
    librarian.remove(User, user)
