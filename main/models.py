from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string

from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.

class User(AbstractUser):
    role_choices = (
        ('organizer', 'Organizer'),
        ('user', 'User')
    )
    role = models.CharField(max_length=10,choices=role_choices, default='user')
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Changed related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Events(models.Model):
    event_name = models.CharField(max_length=50)
    EVENT_CHOICES = (
        ('Music-event', 'Music'),
        ('Educational-event', 'Educational'),
        ('Recreational-event', 'Recreational')
    )
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    event_date = models.DateTimeField(auto_now_add=False)
    event_status = models.BooleanField(default=False)
    event_ticket_quantity = models.PositiveIntegerField(null=True, default=None)
    event_organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    ticket_price = models.DecimalField(decimal_places=5, max_digits=8, null=True, default=None)
    class Meta:
        permissions = [
            ('can_create_event', 'Can create events'),
            ('can_update_event', 'Can update events'),
            ('can_delete_event', 'Can delete events'),
            ('can_read_event', 'Can read events'),
        ]

    def __str__(self):
        return self.event_name

class Tickets(models.Model):
    ticket_id = models.CharField(max_length=10, unique=True)
    ticket_quantity = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(Events, on_delete=models.DO_NOTHING, related_name='tickets', null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    def __str__(self):
        return f'self.ticket_id - ${self.ticket_price}'
    class Meta:
        permissions = [
            ('can_create_ticket', 'Can create tickets'),
            ('can_update_ticket', 'Can update tickets'),
            ('can_delete_ticket', 'Can delete tickets'),
            ('can_read_ticket', 'Can read tickets'),
        ]


@receiver(pre_save, sender=Tickets)
def generate_ticket_id(sender, instance, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = get_random_string(length=10)
        
        # Ensure ticket_id is unique
        while Tickets.objects.filter(ticket_id=instance.ticket_id).exists():
            instance.ticket_id = get_random_string(length=10)