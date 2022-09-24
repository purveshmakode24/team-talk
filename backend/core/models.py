from enum import unique
from django.db import models, transaction
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
# from .utils import get_role_id_by_role_name
from django.utils import timezone
import uuid

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

def get_role_id_by_role_name(role_name):
    try:
        role = Role.objects.get(name=role_name)
        return role.id
    except Exception as e:
        return None

class Role(models.Model):
    name=models.CharField(max_length=255)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """Manager for users. UserManager Used for CLI Integration
    & Other creating and managing objects of the user"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address.')

        # normalize_email() is a helper function that comes
        # with django BaseUserManager class.
        # And it makes the email in lowercase
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # self._db to add multiple dbs
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and saves a new superuser"""
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()  # Assign UserManager to Custom User Model

    USERNAME_FIELD = 'email'


class TeamManager(models.Manager):
    @transaction.atomic
    def create_team(self, name, description, owner_id):
        """Create and save new Team with Admin Membership"""
        if not name:
            raise ValueError('Team must have a name.')

        if not owner_id:
            raise ValueError('Team must have an owner.')

        team = Team(name=name, description=description, owner_id=owner_id)
        team.save(using=self._db)

        # Automatically subscribing TeamMembership as an admin upon Team creation.
        TeamMembership.objects.create(
            user=team.owner,
            team=team,
            role_id=get_role_id_by_role_name('admin')
        )

        return team


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        User, related_name='teams', on_delete=models.CASCADE
    )

    objects = TeamManager()

    def __str__(self):
        return self.name

# @receiver(post_save, sender=Team) # signal
# def create_team_membership(sender, instance, created, **kwargs):
#     """Automatically subscribing TeamMembership as an admin upon Team creation."""
#     if created:
#         TeamMembership.objects.create(
#             user=instance.owner,
#             team=instance,
#             role_id=get_role_id_by_role_name('admin')
#         )

"""
Note: Signal works for both customized code logic and django admin,
but custom Manager won't work in django admin.
To make custom model manager (insted of default manager) to work while
creating new instances from django admin, customize ModelAdmin
by overriding save_form() with few changes.
"""

class TeamMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name='team_memberships', on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team, related_name='team_memberships', on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        Role, related_name='team_memberships', on_delete=models.CASCADE
    )
    joined_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'team'))

    def __str__(self):
        return 'User \'{}\' is a member of \'{}\' having role \'{}\''.format(
            self.user,
            self.team,
            self.role
        )

@receiver(post_delete, sender=TeamMembership) # signal
def delete_team(sender, instance, **kwargs):
    """Automatically deleting a Team if a owner/admin's membership is deleted.
     (reverse foreign-key relation with Team)"""

    # if team membership intance is admin.
    if instance.role.name == 'admin':
        team = Team.objects.get(id=instance.team_id)
        team.delete()


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    created_on = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(
        User, related_name='topics', on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team, related_name='topics', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{}'.format(self.title)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=False)
    created_on = models.DateTimeField(default=timezone.now)
    commented_by = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        Topic, related_name='comments', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment: {}'.format(self.body)




