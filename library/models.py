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


''' 
every user has exactly one user card
user card contains all copies, which user checked out
user card has unique number
'''


class UserCard(models.Model, User):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_card')
    library_card_number = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='user_cards')


class Login(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length=128)