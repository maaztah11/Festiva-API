from rest_framework import serializers
from .models import Events, Tickets
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


from django.contrib.auth import authenticate,login
User = get_user_model()

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ['event', 'ticket_quantity']
        def validate(self, data):
            event = data['event']
            quantity = data['Ticket_quantity']
        
            if event.ticket_event_quantity < quantity:
                raise serializers.ValidationError("Not enough tickets available.")
            return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            role = validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        if user.role == 'organizer':
            self.assign_group_and_permissions(user)
        print(f"User Group(s): {user.groups.all()}")

        return user
    
    def assign_group_and_permissions(self, user):
        group_name = 'Organizers'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        permissions = [
            Permission.objects.get(codename='can_create_event'),
            Permission.objects.get(codename='can_update_event'),
            Permission.objects.get(codename='can_delete_event'),
            Permission.objects.get(codename='can_read_event'),
        ]
        group.permissions.add(*permissions)