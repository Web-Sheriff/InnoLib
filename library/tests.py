from django.test import TestCase

from library.models import *


class TestCaseSettings:
    # def bdclear(self):
    #     Patron.objects.filter().delete()
    #     AudioVideo.objects.filter().delete()
    #     Copy.objects.filter().delete()
    #     Book.objects.filter().delete()
    #     Librarian.objects.filter().delete()
    #     TA.objects.filter().delete()
    #     VisitingProfessor.objects.filter().delete()
    #     Professor.objects.filter().delete()
    #     Instructor.objects.filter().delete()
    #     Document.objects.filter().delete()
    pass


class FirstTestCase(TestCase):
    library = Library.objects.get(id=1)
    # library.save()
    admin = Admin.objects.get(id=1)  # create(login='admin', password='adminadmin', mail='test@yandex.ru', first_name='Salavat', second_name='Vasilev', address='Innopolis', phone_number='88005553535')
    # admin.save()
    librarian = Librarian.objects.first()
    # librarian = admin.add_librarian(login='librarian', password='12345', mail='test@gmail.com', first_name='Librarian', second_name='Librairain', address='Inno', phone_number='1235435', level_of_privileges=2)
    # librarian.send_email(to=['v.vasilev@innopolis.ru', 'n.tupikina@innopolis.ru', 'a.gruk@innopolis.ru'], subject='Test', message='It works!!1!!11!')
    # s1 = librarian.create_user(class_model=Student, login='slavav99', password='653e65hd', first_name='Vyacheslav', second_name='Vasilev', address='Inno', phone_number='+79503201013', mail='slavav99@yandex.ru')
    # b1 = Book.objects.create(library=library, title='NARUTO', price_value='50', is_best_seller=False, edition='4th', publisher='ddd', year='1999')
    # c1 = Copy.objects.create(document=b1, number=2)
    s1 = Student.objects.first()
    b1 = Book.objects.first()
    s1.check_out_doc(b1)
    librarian.handle_book(s1, b1)