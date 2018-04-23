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
    library = Library.objects.create()
    library.save()
    # library = Library.objects.get(id=1)

    admin = Admin.objects.create(login='admin', password='adminadmin', mail='test@yandex.ru', first_name='Vyacheslav', second_name='Vasilev', address='Innopolis', phone_number='88005553535')
    user_card = UserCard.objects.create(user=admin, library=library, library_card_number=0)
    user_card.save()
    admin.save()
    # admin = Admin.objects.get(id=1)

    librarian = admin.add_librarian(login='librarian', password='12345', mail='test@gmail.com', first_name='Alexander', second_name='Gruk', address='Innopolis', phone_number='1235435', level_of_privileges=3)
    librarian.save()
    # librarian = Librarian.objects.first()

    s1 = librarian.create_user(class_model=Student, login='student', password='qwerty', first_name='Natalia', second_name='Tupikina', address='Innopolis', phone_number='+654374321', mail='test@mail.ru')
    s1.save()
    # s1 = Student.objects.first()

    a1 = librarian.create_author(name='Masashi Kishimoto')
    a2 = librarian.create_author(name='Tolkien')
    a3 = librarian.create_author(name='Dawg')
    a4 = librarian.create_author(name='Tolstoy')
    a5 = librarian.create_author(name='Bulgakov')
    a6 = librarian.create_author(name='Pushkin')
    a7 = librarian.create_author(name='King')
    a8 = librarian.create_author(name='Chekhov')
    a9 = librarian.create_author(name='Shakespear')
    a10 = librarian.create_author(name='Gogol')
    a11 = librarian.create_author(name='Dostoevsky')

    authors1 = Author.objects.all()[:2]
    authors2 = Author.objects.all()[1:3]
    authors3 = Author.objects.all()[1:4]
    authors4 = Author.objects.all()[4:6]
    authors5 = Author.objects.all()[3:7]
    authors6 = Author.objects.all()[6:10]
    authors7 = Author.objects.all()[5:8]
    authors8 = Author.objects.all()[2:6]
    authors9 = Author.objects.all()[4:11]
    authors10 = Author.objects.all()[5:12]
    authors11 = Author.objects.all()[3:9]

    # a1 = Author.objects.get(id=1)
    # a2 = Author.objects.get(id=2)
    # a3 = Author.objects.get(id=3)
    # a4 = Author.objects.get(id=4)
    # a5 = Author.objects.get(id=5)
    # a6 = Author.objects.get(id=6)
    # a7 = Author.objects.get(id=7)
    # a8 = Author.objects.get(id=8)
    # a9 = Author.objects.get(id=9)
    # a10 = Author.objects.get(id=10)
    # a11 = Author.objects.get(id=11)

    b1 = librarian.create_book_new(library=library, is_best_seller=False, title='Naruto', price_value='50', edition='4th', publisher='ddd', year='1999', reference=False, authors=authors1)
    b1.save()
    librarian.create_copies(b1, 2)
    b2 = librarian.create_book_new(library=library, is_best_seller=True, title='451', price_value='55', edition='1th', publisher='ttt', year='2017', reference=False, authors=authors2)
    b2.save()
    librarian.create_copies(b2, 3)
    b3 = librarian.create_book_new(library=library, is_best_seller=False, title='1984', price_value='57', edition='5th', publisher='sss', year='2015', reference=False, authors=authors3)
    b3.save()
    librarian.create_copies(b3, 1)
    b4 = librarian.create_book_new(library=library, is_best_seller=True, title='Portret', price_value='43', edition='3th', publisher='xxx', year='2012', reference=False, authors=authors4)
    b4.save()
    librarian.create_copies(b4, 2)
    b5 = librarian.create_book_new(library=library, is_best_seller=True, title='Vino', price_value='21', edition='2th', publisher='ccc', year='2018', reference=False, authors=authors5)
    b5.save()
    librarian.create_copies(b5, 4)
    b6 = librarian.create_book_new(library=library, is_best_seller=False, title='Shantaram', price_value='87', edition='5th', publisher='zzz', year='2008', reference=False, authors=authors6)
    b6.save()
    librarian.create_copies(b6, 3)
    b7 = librarian.create_book_new(library=library, is_best_seller=False, title='Anna', price_value='54', edition='4th', publisher='rrr', year='2013', reference=False, authors=authors7)
    b7.save()
    librarian.create_copies(b7, 1)
    b8 = librarian.create_book_new(library=library, is_best_seller=True, title='Shadow', price_value='78', edition='1th', publisher='hhh', year='2007', reference=False, authors=authors8)
    b8.save()
    librarian.create_copies(b8, 2)
    b9 = librarian.create_book_new(library=library, is_best_seller=True, title='Prestyplenie', price_value='59', edition='2th', publisher='iii', year='2006', reference=False, authors=authors9)
    b9.save()
    librarian.create_copies(b9, 4)
    b10 = librarian.create_book_new(library=library, is_best_seller=False, title='Atlant', price_value='61', edition='1th', publisher='ppp', year='2001', reference=False, authors=authors10)
    b10.save()
    librarian.create_copies(b10, 3)
    b11 = librarian.create_book_new(library=library, is_best_seller=False, title='Arka', price_value='28', edition='7th', publisher='ppp', year='2003', reference=False, authors=authors11)
    b11.save()
    librarian.create_copies(b11, 2)

    # b1 = Book.objects.get(id=1)
    # b2 = Book.objects.get(id=2)
    # b3 = Book.objects.get(id=3)
    # b4 = Book.objects.get(id=4)
    # b5 = Book.objects.get(id=5)
    # b6 = Book.objects.get(id=6)
    # b7 = Book.objects.get(id=7)
    # b8 = Book.objects.get(id=8)
    # b9 = Book.objects.get(id=9)
    # b10 = Book.objects.get(id=10)
    # b11 = Book.objects.get(id=11)

    s1.check_out_doc(b1)
    s1.check_out_doc(b4)
    s1.check_out_doc(b3)
    s1.check_out_doc(b5)
    s1.check_out_doc(b4)
    s1.check_out_doc(b8)
    s1.check_out_doc(b11)
    s1.check_out_doc(b11)
    s1.check_out_doc(b7)
    s1.check_out_doc(b9)

    librarian.handle_book(s1, b1)
    librarian.handle_book(s1, b4)
    librarian.handle_book(s1, b3)
    librarian.handle_book(s1, b5)
    librarian.handle_book(s1, b4)
    librarian.handle_book(s1, b8)
    librarian.handle_book(s1, b11)
    librarian.handle_book(s1, b11)
    librarian.handle_book(s1, b7)
    librarian.handle_book(s1, b9)
    librarian.accept_doc(s1, b1)
    librarian.outstanding_request(b7)
    print(s1.search_by_author_and_title(title='naru', author='tolk'))
