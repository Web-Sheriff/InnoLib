# from django.test import TestCase

from library.models import *


'''
TestCase Settings:
    set_up - library and admin creating
    bd_clear - database cleaning
    kwargs - predefined dictionaries whose keys becoming arguments while objects creating
'''


class TestCaseSettings:
    @staticmethod
    def set_up():
        if Library.objects.first() is None:
            library = Library.objects.create()
            library.save()
        else:
            library = Library.objects.first()
        logging.info("Innopolis Library starts working")
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

    'kwargs for users and documents creating'

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
                "password": "123456789", "address": "Avenida Mazatlan, 250", "phone_number": "30004",
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


'''
Test Cases
Every Test Case has only 3 static features:
    set_up() - test case initial states set up 
    test_case() - test case actions
    bd_clear() - database clearing
'''


'First Test Case'


class FirstTestCase:
    @staticmethod
    def set_up():
        logging.info("First Test Case")
        TestCaseSettings.set_up()

    @staticmethod
    def test_case():
        library = Library.objects.first()
        library.create_admin()

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Second Test Case'


class SecondTestCase:
    @staticmethod
    def set_up():
        logging.info("Second Test Case")
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


'Third Test Case'


class ThirdTestCase:
    @staticmethod
    def set_up():
        logging.info("Third Test Case")
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

        l1.check_information_of_the_system()

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Fourth Test Case'


class FourthTestCase:
    @staticmethod
    def set_up():
        logging.info("Fourth Test Case")
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

        l2.check_information_of_the_system()

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Fifth Test Case'


class FifthTestCase:
    @staticmethod
    def set_up():
        logging.info("Fifth Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        l2 = Librarian.objects.get(login='lib2')
        l3 = Librarian.objects.get(login='lib3')
        d1 = Book.objects.get(year='2009')

        l3.remove_copies(d1, 1)

        l2.check_information_of_the_system()

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Sixth Test Case'


class SixthTestCase:
    @staticmethod
    def set_up():
        logging.info("Sixth Test Case")
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


'Seventh Test Case'


class SeventhTestCase:
    @staticmethod
    def set_up():
        logging.info("Seventh Test Case")
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


'Eighth Test Case'


class EighthTestCase:
    @staticmethod
    def set_up():
        logging.info("Eighth Test Case")
        SixthTestCase.set_up()
        SixthTestCase.test_case()

    @staticmethod
    def test_case():
        admin1 = Admin.objects.first()
        admin1.check_logs_for_tests('Eighth Test Case')

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Ninth Test Case'


class NinthTestCase:
    @staticmethod
    def set_up():
        logging.info("Ninth Test Case")
        SeventhTestCase.set_up()
        SeventhTestCase.test_case()

    @staticmethod
    def test_case():
        admin1 = Admin.objects.first()
        admin1.check_logs_for_tests('Ninth Test Case')

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Tenth Test Case'


class TenthTestCase:
    @staticmethod
    def set_up():
        logging.info("Tenth Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        v = VisitingProfessor.objects.get(login='visit1')
        search_res = v.search_by_title('Introduction to Algorithms')

        counter = 1
        for res in search_res:
            print(str(counter) + '. ' + res.title + ' by ' + res.authors.first().name + '.')
            counter += 1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Eleventh Test Case'


class EleventhTestCase:
    @staticmethod
    def set_up():
        logging.info("Eleventh Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        v = VisitingProfessor.objects.get(login='visit1')
        search_res = v.search_by_title('Algorithms')

        counter = 1
        for res in search_res:
            print(str(counter) + '. ' + res.title + ' by ' + res.authors.first().name + '.')
            counter += 1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Twelfth Test Case'


class TwelfthTestCase:
    @staticmethod
    def set_up():
        logging.info("Twelfth Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        v = VisitingProfessor.objects.get(login='visit1')
        keywords = Keyword.objects.filter(word='Algorithms')
        search_res = v.search_by_keywords(keywords)

        counter = 1
        for res in search_res:
            print(str(counter) + '. ' + res.title + ' by ' + res.authors.first().name)
            counter += 1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Thirteenth Test Case'


class ThirteenthTestCase:
    @staticmethod
    def set_up():
        logging.info("Thirteenth Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        v = VisitingProfessor.objects.get(login='visit1')
        titles = ['Algorithms', 'Programming']
        search_res = v.search_by_titles_and(titles)

        counter = 1
        for res in search_res:
            print(str(counter) + '. ' + res.title + ' by ' + res.authors.first().name + '.')
            counter += 1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'Fourteenth Test Case'


class FourteenthTestCase:
    @staticmethod
    def set_up():
        logging.info("Fourteenth Test Case")
        FourthTestCase.set_up()
        FourthTestCase.test_case()

    @staticmethod
    def test_case():
        v = VisitingProfessor.objects.get(login='visit1')
        titles = ['Algorithms', 'Programming']
        search_res = v.search_by_titles_or(titles)

        counter = 1
        for res in search_res:
            print(str(counter) + '. ' + res.title + ' by ' + res.authors.first().name + '.')
            counter += 1

    @staticmethod
    def bd_clear():
        TestCaseSettings.bd_clear()


'''
Test Cases initializations
'''


'First Test Case initialization'

print("First Test Case")
FirstTestCase.bd_clear()
FirstTestCase.set_up()
FirstTestCase.test_case()
FirstTestCase.bd_clear()

'Second Test Case initialization'

print("Second Test Case")
SecondTestCase.bd_clear()
SecondTestCase.set_up()
SecondTestCase.test_case()
SecondTestCase.bd_clear()

'Third Test Case initialization'

print("Third Test Case")
ThirdTestCase.bd_clear()
ThirdTestCase.set_up()
ThirdTestCase.test_case()
ThirdTestCase.bd_clear()

'Fourth Test Case initialization'

print("Fourth Test Case")
FourthTestCase.bd_clear()
FourthTestCase.set_up()
FourthTestCase.test_case()
FourthTestCase.bd_clear()

'Fifth Test Case initialization'

print("Fifth Test Case")
FifthTestCase.bd_clear()
FifthTestCase.set_up()
FifthTestCase.test_case()
FifthTestCase.bd_clear()

'Sixth Test Case initialization'

print("Sixth Test Case")
SixthTestCase.bd_clear()
SixthTestCase.set_up()
SixthTestCase.test_case()
SixthTestCase.bd_clear()

'Seventh Test Case initialization'

print("Seventh Test Case")
SeventhTestCase.bd_clear()
SeventhTestCase.set_up()
SeventhTestCase.test_case()
SeventhTestCase.bd_clear()

'Eighth Test Case initialization'

print("Eighth Test Case")
EighthTestCase.bd_clear()
EighthTestCase.set_up()
EighthTestCase.test_case()
EighthTestCase.bd_clear()

'Ninth Test Case initialization'

print("Ninth Test Case")
NinthTestCase.bd_clear()
NinthTestCase.set_up()
NinthTestCase.test_case()
NinthTestCase.bd_clear()

'Tenth Test Case initialization'

print("Tenth Test Case")
TenthTestCase.bd_clear()
TenthTestCase.set_up()
TenthTestCase.test_case()
TenthTestCase.bd_clear()

'Eleventh Test Case initialization'

print("Eleventh Test Case")
EleventhTestCase.bd_clear()
EleventhTestCase.set_up()
EleventhTestCase.test_case()
EleventhTestCase.bd_clear()

'Twelfth Test Case initialization'

print("Twelfth Test Case")
TwelfthTestCase.bd_clear()
TwelfthTestCase.set_up()
TwelfthTestCase.test_case()
TwelfthTestCase.bd_clear()

'Thirteenth Test Case initialization'

print("Thirteenth Test Case")
ThirteenthTestCase.bd_clear()
ThirteenthTestCase.set_up()
ThirteenthTestCase.test_case()
ThirteenthTestCase.bd_clear()

'Fourteenth Test Case initialization'

print("Fourteenth Test Case")
FourteenthTestCase.bd_clear()
FourteenthTestCase.set_up()
FourteenthTestCase.test_case()
FourteenthTestCase.bd_clear()
