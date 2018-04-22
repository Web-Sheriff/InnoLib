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
    # library = Library.objects.create()
    library = Library.objects.get(id=1)
    # library.save()
    #
    admin = Admin.objects.get(id=1)
    # admin = Admin.objects.create(login='admin', password='adminadmin', mail='test@yandex.ru', first_name='Salavat', second_name='Vasilev', address='Innopolis', phone_number='88005553535')
    # user_card = UserCard.objects.create(user=admin, library=library, library_card_number=0)
    # user_card.save()
    # admin.save()
    librarian = Librarian.objects.first()
    # librarian = admin.add_librarian(login='librarian', password='12345', mail='test@gmail.com', first_name='Librarian', second_name='Librairain', address='Inno', phone_number='1235435', level_of_privileges=2)
    # librarian.save()
    #
    # librarian.send_email(to=['v.vasilev@innopolis.ru', 'n.tupikina@innopolis.ru', 'a.gruk@innopolis.ru'], subject='Test', message='It works!!1!!11!')
    #
    # s1 = librarian.create_user(class_model=Student, login='slavav99', password='653e65hd', first_name='Vyacheslav', second_name='Vasilev', address='Inno', phone_number='+79503201013', mail='slavav99@yandex.ru')
    # a1 = Author.objects.create(name='Masashi Kishimoto')
    # a2 = Author.objects.create(name='Tolkien')
    # a3 = Author.objects.create(name='Dawg')
    a1 = Author.objects.get(id=1)
    a2 = Author.objects.get(id=2)
    a3 = Author.objects.get(id=3)
    authors1 = Author.objects.all()[:2]
    authors2 = Author.objects.all()[1:3]
    # b1 = librarian.create_book(library=library, title='NARUTO', price_value='50', is_best_seller=False, edition='4th', publisher='ddd', year='1999', reference=False, authors=authors1)
    # b1.save()
    # s1.save()
    b1 = Book.objects.get(id=1)
    b2 = Book.objects.get(id=2)
    s1 = Student.objects.first()
    # librarian.create_copies(b1, 2)
    # b2 = librarian.create_book(library=library, is_best_seller=True, title='BORUTO', price_value='55', edition='1th', publisher='Masashi', year='2017', reference=False, authors=authors2)
    # librarian.create_copies(b2, 3)
    # b2.save()
    s1.check_out_doc(b1)
    librarian.handle_book(s1, b1)
