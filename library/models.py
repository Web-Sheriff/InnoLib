from django.db import models

from users.models import User


class Library(models.Model):
    def count_unchecked_copies(self, doc):
        return len(doc.copies.filter(is_checked_out=False))

    def calculate_users_items(self, user):
        return len(user.copies.all())

    def is_due(self):
        pass

    def overdue_fines(self):
        pass
    
    def count_unchecked_copies (self, doc):
        a = 0
        for copy in doc.copies.all():
            if not copy.is_checked_out:
                a += 1
        return a

    def calculate_users_items(self, user):
        a = 0
        for copy in user.user_card.copies.all():
            a += 1
        return a

    def is_due(self):
        pass

    def overdue_fines(self):
        pass


''' 
every user has exactly one user card
user card contains all copies, which user checked out
user card has unique number
'''


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_card')
    library_card_number = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='user_cards')


class Login(models.Model):
 username = models.EmailField()
 password = models.CharField(max_length=128)