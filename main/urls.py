from django.urls import path
from .views import EventView, TicketCreateView, EventList, EventUpdateView, TicketListView, GetUsers, EventDeleteView, TicketDeleteView, LoginUserView,TicketUpdateView, SignUser
urlpatterns = [
    path('ticket_create/', TicketCreateView.as_view(), name='ticket-create'),
    path('event/', EventView.as_view(), name='event-create'),
    path('event_update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('event_delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
     path('ticket_update/<int:pk>/', TicketUpdateView.as_view(), name='event-update'),
    path('ticket_delete/<int:pk>/', TicketDeleteView.as_view(), name='event-delete'),
    path('signup/', SignUser.as_view(), name='sign' ),
    path('login/',LoginUserView.as_view(), name='login' ),
    path('user_list/',GetUsers.as_view(), name='user-list' ),
    path('event_list/', EventList.as_view(), name='event-list'),
    path('ticket_list/',TicketListView.as_view(), name='ticket-list' )
]