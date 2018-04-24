# from django.test import TestCase

from library.models import *


class TestCaseSettings:
    @staticmethod
    def set_up():
        if Library.objects.first() is None:
            library = Library.objects.create()
            library.save()
        else:
            library = Library.objects.first()
        library.create_admin()

    @staticmethod
    def bd_clear():
        Library.objects.all().delete()
        User.objects.all().delete()
        Document.objects.all().delete()
        Author.objects.all().delete()
        Editor.objects.all().delete()
        Issue.objects.all().delete()
        Journal.objects.all().delete()
        Keyword.objects.all().delete()
        Login.objects.all().delete()

    '''kwargs for users and documents creating'''

    d1_authors_names = ["Thomas H. Cormen", "Charles E. Leiserson", "Ronald L. Rivest", "Clifford Stein"]
    d2_authors_names = ["Niklaus Wirth"]
    d3_authors_names = ["Donald E. Knuth"]

    d1_keywords_words = ["Algorithms", "Data Structures", "Complexity", "Computational Theory"]
    d2_keywords_words = ["Algorithms", "Data Structures", "Search Algorithms", "Pascal"]
    d3_keywords_words = ["Algorithms", "Combinatorial Algorithms", "Recursion"]

    d1_kwargs = {"is_best_seller": False, "reference": False, "title": "Introduction to Algorithms",
                 "price_value": 5000, "edition": "Third edition", "publisher": "MIT Press",
                 "year": '2009', "authors": d1_authors_names, "keywords": d1_keywords_words}
    d2_kwargs = {"is_best_seller": False, "reference": False, "title": "Algorithms + Data Structures = Programs",
                 "price_value": 5000, "edition": "First edition", "publisher": "Prentice Hall PTR",
                 "year": '1978', "authors": d2_authors_names, "keywords": d2_keywords_words}
    d3_kwargs = {"is_best_seller": False, "reference": False, "title": "The Art of Computer Programming",
                 "price_value": 5000, "edition": "Third edition", "publisher": "Addison Wesley Longman Publishing Co., Inc.",
                 "year": '1997', "authors": d3_authors_names, "keywords": d3_keywords_words}

    p1_kwargs = {"class_model": Professor, "first_name": "Sergey", "second_name": "Afonso",
                 "login": "prof1", "password": "123qwe", "address": "Via Margutta, 3", "phone_number": "30001",
                 "mail": "sergey_afonso@gmail.com", "library_card_number": 1010}
    p2_kwargs = {"class_model": Professor, "first_name": "Nadia", "second_name": "Teixeira",
                 "login": "prof2", "password": "12345", "address": "Via Sacra, 13", "phone_number": "30002",
                 "mail": "nadia_teixeira@gmail.com", "library_card_number": 1011}
    p3_kwargs = {"class_model": Professor, "first_name": "Elvira", "second_name": "Espindola",
                 "login": "prof3", "password": "qwerty", "address": "Via del Corso, 22", "phone_number": "30003",
                 "mail": "elvira_espindola@gmail.com", "library_card_number": 1100}

    s_kwargs = {"class_model": Student, "first_name": "Andrey", "second_name": "Velo", "login": "stud1",
                "password": "qwertyu", "address": "Avenida Mazatlan, 250", "phone_number": "30004",
                "mail": "andrey_velo@gmail.com", "library_card_number": 1101}
    v_kwargs = {"class_model": VisitingProfessor, "first_name": "Veronika", "second_name": "Rama",
                "login": "visit1", "password": "12345qwe", "address": "Street Atocha, 27",
                "phone_number": "30005", "mail": "veronika_rama@gmail.com", "library_card_number": 1110}

    l1_kwargs = {"first_name": "Eugenia", "second_name": "Rama",
                 "login": "lib1", "password": "123qwerty", "address": "Naberezhnochelninskiy Avenue, 7", "phone_number": "30006",
                 "mail": "anton_khvorov@gmail.com", "level_of_privileges": 1}
    l2_kwargs = {"first_name": "Luie", "second_name": "Ramos",
                 "login": "lib2", "password": "qwerty123", "address": "Universitetskaya Street, 1", "phone_number": "30007",
                 "mail": "alexander_gruk@gmail.com", "level_of_privileges": 2}
    l3_kwargs = {"first_name": "Ramon", "second_name": "Valdez",
                 "login": "lib3", "password": "qwe12345", "address": "K. Marks Street, 4", "phone_number": "30008",
                 "mail": "natalya_tupikina@gmail.com", "level_of_privileges": 3}

    '''Test Cases'''


class FirstTestCase:
    @staticmethod
    def set_up():
        TestCaseSettings.set_up()

    @staticmethod
    def test_case():
        library = Library.objects.first()
        library.create_admin()

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class SecondTestCase:
    @staticmethod
    def set_up():
        TestCaseSettings.set_up()

    @staticmethod
    def test_case():
        admin = Admin.objects.first()
        admin.add_librarian(**TestCaseSettings.l1_kwargs)
        admin.add_librarian(**TestCaseSettings.l2_kwargs)
        admin.add_librarian(**TestCaseSettings.l3_kwargs)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class ThirdTestCase:
    @staticmethod
    def set_up():
        SecondTestCase.set_up()
        SecondTestCase.test_case()

    @staticmethod
    def test_case():
        l1 = Librarian.objects.get(login='lib1')

        d1 = l1.create_book_with_authors_names(**TestCaseSettings.d1_kwargs)
        d2 = l1.create_book_with_authors_names(**TestCaseSettings.d2_kwargs)
        d3 = l1.create_book_with_authors_names(**TestCaseSettings.d3_kwargs)

        l1.create_copies(document=d1, number=3)
        l1.create_copies(document=d2, number=3)
        l1.create_copies(document=d3, number=3)

        # l1 checks the information of the system. I dunno what is it, but we need this feature (i will implement this later)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class FourthTestCase:
    @staticmethod
    def set_up():
        SecondTestCase.set_up()
        SecondTestCase.test_case()

    @staticmethod
    def test_case():
        l2 = Librarian.objects.get(login='lib2')

        d1 = l2.create_book_with_authors_names(**TestCaseSettings.d1_kwargs)
        d2 = l2.create_book_with_authors_names(**TestCaseSettings.d2_kwargs)
        d3 = l2.create_book_with_authors_names(**TestCaseSettings.d3_kwargs)

        l2.create_copies(document=d1, number=3)
        l2.create_copies(document=d2, number=3)
        l2.create_copies(document=d3, number=3)

        l2.create_user_with_library_card_number(**TestCaseSettings.s_kwargs)
        l2.create_user_with_library_card_number(**TestCaseSettings.p1_kwargs)
        l2.create_user_with_library_card_number(**TestCaseSettings.p2_kwargs)
        l2.create_user_with_library_card_number(**TestCaseSettings.p3_kwargs)
        l2.create_user_with_library_card_number(**TestCaseSettings.v_kwargs)

        # l2 checks the information of the system. I dunno what is it, but we need this feature (i will implement this later)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class FifthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        l2 = Librarian.objects.get(login='lib2')
        l3 = Librarian.objects.get(login='lib3')
        d1 = Book.objects.get(year='2009')

        l3.remove_copies(d1, 1)

        # l2 checks the information of the system. I dunno what is it, but we need this feature (i will implement this later)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class SixthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        p1 = Professor.objects.get(login='prof1')
        p2 = Professor.objects.get(login='prof2')
        p3 = Professor.objects.get(login='prof3')
        s = Student.objects.get(login='stud1')
        v = VisitingProfessor.objects.get(login='visit1')
        l1 = Librarian.objects.get(login='lib1')
        d3 = Book.objects.get(year='1997')

        p1.check_out_doc(d3)
        l1.handle_book(p1, d3)
        p2.check_out_doc(d3)
        l1.handle_book(p2, d3)
        s.check_out_doc(d3)
        l1.handle_book(s, d3)
        v.check_out_doc(d3)
        l1.handle_book(v, d3)
        p3.check_out_doc(d3)
        l1.handle_book(p3, d3)

        l1.outstanding_request(d3)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class SeventhTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        p1 = Professor.objects.get(login='prof1')
        p2 = Professor.objects.get(login='prof2')
        p3 = Professor.objects.get(login='prof3')
        s = Student.objects.get(login='stud1')
        v = VisitingProfessor.objects.get(login='visit1')
        l3 = Librarian.objects.get(login='lib3')
        d3 = Book.objects.get(year='1997')

        p1.check_out_doc(d3)
        l3.handle_book(p1, d3)
        p2.check_out_doc(d3)
        l3.handle_book(p2, d3)
        s.check_out_doc(d3)
        l3.handle_book(s, d3)
        v.check_out_doc(d3)
        l3.handle_book(v, d3)
        p3.check_out_doc(d3)
        l3.handle_book(p3, d3)

        l3.outstanding_request(d3)

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class EighthTestCase:
    @staticmethod
    def set_up():
        SixthTestCase.set_up()
        SixthTestCase.test_case()

    @staticmethod
    def test_case():
        admin1 = Admin.objects.first()
        admin1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class NinthTestCase:
    @staticmethod
    def set_up():
        SeventhTestCase.set_up()
        SeventhTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class TenthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class EleventhTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class TwelfthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class ThirteenthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


class FourteenthTestCase:
    @staticmethod
    def set_up():
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        pass

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


# TestCaseSettings.bd_clear()
# FirstTestCase.set_up()
# FirstTestCase.test_case()
# FirstTestCase.bd_clear()
#
#
# TestCaseSettings.bd_clear()
# SecondTestCase.set_up()
# SecondTestCase.test_case()
# SecondTestCase.bd_clear()
#
#
# TestCaseSettings.bd_clear()
# ThirdTestCase.set_up()
# ThirdTestCase.test_case()
# ThirdTestCase.bd_clear()
#
#
# TestCaseSettings.bd_clear()
# FourthTestCase.set_up()
# FourthTestCase.test_case()
# FourthTestCase.bd_clear()
#
#
# TestCaseSettings.bd_clear()
# FifthTestCase.set_up()
# FifthTestCase.test_case()
# FifthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# SixthTestCase.set_up()
# SixthTestCase.test_case()
# SixthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# SeventhTestCase.set_up()
# SeventhTestCase.test_case()
# SeventhTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# EighthTestCase.set_up()
# EighthTestCase.test_case()
# EighthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# NinthTestCase.set_up()
# NinthTestCase.test_case()
# NinthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# TenthTestCase.set_up()
# TenthTestCase.test_case()
# TenthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# EleventhTestCase.set_up()
# EleventhTestCase.test_case()
# EleventhTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# TwelfthTestCase.set_up()
# TwelfthTestCase.test_case()
# TwelfthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# ThirteenthTestCase.set_up()
# ThirteenthTestCase.test_case()
# ThirteenthTestCase.bd_clear()


# TestCaseSettings.bd_clear()
# FourteenthTestCase.set_up()
# FourteenthTestCase.test_case()
# FourteenthTestCase.bd_clear()


# class TestTestCase(TestCase):
#     TestCaseSettings.set_up()
#     # library = Library.objects.create()
#     # library.save()
#     library = Library.objects.get(id=1)
#
#     # admin = library.create_admin()
#     admin = Admin.objects.first()
#
#     # librarian = admin.add_librarian(login='librarian', password='12345', mail='test@gmail.com', first_name='Alexander', second_name='Gruk', address='Innopolis', phone_number='1235435', level_of_privileges=3)
#     # librarian.save()
#     librarian = Librarian.objects.first()
#     #
#     # s1 = librarian.create_user(class_model=Student, login='student', password='qwerty', first_name='Natalia', second_name='Tupikina', address='Innopolis', phone_number='+654374321', mail='test@mail.ru')
#     # s1.save()
#     s1 = Student.objects.first()
#     #
#     # a1 = librarian.create_author(name='Masashi Kishimoto')
#     # a2 = librarian.create_author(name='Tolkien')
#     # a3 = librarian.create_author(name='Dawg')
#     # a4 = librarian.create_author(name='Tolstoy')
#     # a5 = librarian.create_author(name='Bulgakov')
#     # a6 = librarian.create_author(name='Pushkin')
#     # a7 = librarian.create_author(name='King')
#     # a8 = librarian.create_author(name='Chekhov')
#     # a9 = librarian.create_author(name='Shakespear')
#     # a10 = librarian.create_author(name='Gogol')
#     # a11 = librarian.create_author(name='Dostoevsky')
#     #
#     # authors1 = Author.objects.all()[:2]
#     # authors2 = Author.objects.all()[1:3]
#     # authors3 = Author.objects.all()[1:4]
#     # authors4 = Author.objects.all()[4:6]
#     # authors5 = Author.objects.all()[3:7]
#     # authors6 = Author.objects.all()[6:10]
#     # authors7 = Author.objects.all()[5:8]
#     # authors8 = Author.objects.all()[2:6]
#     # authors9 = Author.objects.all()[4:11]
#     # authors10 = Author.objects.all()[5:12]
#     # authors11 = Author.objects.all()[3:9]
#     #
#     a1 = Author.objects.get(id=1)
#     a2 = Author.objects.get(id=2)
#     a3 = Author.objects.get(id=3)
#     a4 = Author.objects.get(id=4)
#     a5 = Author.objects.get(id=5)
#     a6 = Author.objects.get(id=6)
#     a7 = Author.objects.get(id=7)
#     a8 = Author.objects.get(id=8)
#     a9 = Author.objects.get(id=9)
#     a10 = Author.objects.get(id=10)
#     a11 = Author.objects.get(id=11)
#     #
#     # b1 = librarian.create_book_new(library=library, is_best_seller=False, title='Naruto', price_value='50', edition='4th', publisher='ddd', year='1999', reference=False, authors=authors1)
#     # b1.save()
#     # librarian.create_copies(b1, 2)
#     # b2 = librarian.create_book_new(library=library, is_best_seller=True, title='451', price_value='55', edition='1th', publisher='ttt', year='2017', reference=False, authors=authors2)
#     # b2.save()
#     # librarian.create_copies(b2, 3)
#     # b3 = librarian.create_book_new(library=library, is_best_seller=False, title='1984', price_value='57', edition='5th', publisher='sss', year='2015', reference=False, authors=authors3)
#     # b3.save()
#     # librarian.create_copies(b3, 1)
#     # b4 = librarian.create_book_new(library=library, is_best_seller=True, title='Portret', price_value='43', edition='3th', publisher='xxx', year='2012', reference=False, authors=authors4)
#     # b4.save()
#     # librarian.create_copies(b4, 2)
#     # b5 = librarian.create_book_new(library=library, is_best_seller=True, title='Vino', price_value='21', edition='2th', publisher='ccc', year='2018', reference=False, authors=authors5)
#     # b5.save()
#     # librarian.create_copies(b5, 4)
#     # b6 = librarian.create_book_new(library=library, is_best_seller=False, title='Shantaram', price_value='87', edition='5th', publisher='zzz', year='2008', reference=False, authors=authors6)
#     # b6.save()
#     # librarian.create_copies(b6, 3)
#     # b7 = librarian.create_book_new(library=library, is_best_seller=False, title='Anna', price_value='54', edition='4th', publisher='rrr', year='2013', reference=False, authors=authors7)
#     # b7.save()
#     # librarian.create_copies(b7, 1)
#     # b8 = librarian.create_book_new(library=library, is_best_seller=True, title='Shadow', price_value='78', edition='1th', publisher='hhh', year='2007', reference=False, authors=authors8)
#     # b8.save()
#     # librarian.create_copies(b8, 2)
#     # b9 = librarian.create_book_new(library=library, is_best_seller=True, title='Prestyplenie', price_value='59', edition='2th', publisher='iii', year='2006', reference=False, authors=authors9)
#     # b9.save()
#     # librarian.create_copies(b9, 4)
#     # b10 = librarian.create_book_new(library=library, is_best_seller=False, title='Atlant', price_value='61', edition='1th', publisher='ppp', year='2001', reference=False, authors=authors10)
#     # b10.save()
#     # librarian.create_copies(b10, 3)
#     # b11 = librarian.create_book_new(library=library, is_best_seller=False, title='Arka', price_value='28', edition='7th', publisher='ppp', year='2003', reference=False, authors=authors11)
#     # b11.save()
#     # librarian.create_copies(b11, 2)
#     #
#     b1 = Book.objects.get(id=1)
#     b2 = Book.objects.get(id=2)
#     b3 = Book.objects.get(id=3)
#     b4 = Book.objects.get(id=4)
#     b5 = Book.objects.get(id=5)
#     b6 = Book.objects.get(id=6)
#     b7 = Book.objects.get(id=7)
#     b8 = Book.objects.get(id=8)
#     b9 = Book.objects.get(id=9)
#     b10 = Book.objects.get(id=10)
#     b11 = Book.objects.get(id=11)
#     #
#     # s1.check_out_doc(b1)
#     # s1.check_out_doc(b4)
#     # s1.check_out_doc(b3)
#     # s1.check_out_doc(b5)
#     # s1.check_out_doc(b4)
#     # s1.check_out_doc(b8)
#     # s1.check_out_doc(b11)
#     # s1.check_out_doc(b11)
#     # s1.check_out_doc(b7)
#     # s1.check_out_doc(b9)
#     #
#     # librarian.handle_book(s1, b1)
#     # librarian.handle_book(s1, b4)
#     # librarian.handle_book(s1, b3)
#     # librarian.handle_book(s1, b5)
#     # librarian.handle_book(s1, b4)
#     # librarian.handle_book(s1, b8)
#     # librarian.handle_book(s1, b11)
#     # librarian.handle_book(s1, b11)
#     # librarian.handle_book(s1, b7)
#     # librarian.handle_book(s1, b9)
#     # librarian.accept_doc(s1, b1)
#     # librarian.outstanding_request(b7)
#     # print(s1.search_by_author_and_title(title='naru', author='tolk'))
#     TestCaseSettings.bd_clear()
