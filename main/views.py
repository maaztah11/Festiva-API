from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Events, Tickets
from .serializers import EventSerializer, TicketSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


# Create your views here.
User = get_user_model()
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        user_role = getattr(user, 'role', None) 
        print(user_role) # Use getattr to handle cases where 'role' might not exist
        if user_role != 'organizer':
            return Response({"detail": "Only organizers can create events."}, status=status.HTTP_403_FORBIDDEN)
        request.data['event_organizer'] = request.user.id
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EventList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    #Allowing filtering of events
    filterset_fields = ['event_name', 'event_type']
    #order events
    ordering_fields = ['event_date', 'event_type']
    #search events
    search_fields = [  '^event_name',]
@method_decorator(permission_required('can_update_event', raise_exception=True), name='put')
class EventUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(permission_required('can_delete_event', raise_exception=True), name='delete')
class EventDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class TicketCreateView(generics.CreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        quantity = serializer.validated_data['ticket_quantity']
        
        # Update the available tickets
        event.event_ticket_quantity -= int(quantity)
        event.save()
        
        # Save the ticket booking
        serializer.save(user=self.request.user)
class TicketDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        ticket = get_object_or_404(Tickets, pk=pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class TicketUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        ticket = get_object_or_404(Tickets, pk=pk)
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error)
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user
        return Tickets.objects.filter(user=user)
class SignUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }
            
            # Add a custom claim if the user is an organizer
            if user.role == 'organizer':
                response_data['is_organizer'] = True
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class GetUsers(APIView):
  def get(self, request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

