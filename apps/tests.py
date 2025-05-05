from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from .models import Event


class EventTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

        # Create an event for user1
        self.event1 = Event.objects.create(
            title='Test Event 1',
            description='Description for test event 1',
            date=datetime.now() + timedelta(days=10),
            location='Test Location 1',
            created_by=self.user1
        )

        # Create an event for user2
        self.event2 = Event.objects.create(
            title='Test Event 2',
            description='Description for test event 2',
            date=datetime.now() + timedelta(days=20),
            location='Test Location 2',
            created_by=self.user2
        )

        # Set up authentication tokens
        self.user1_token = RefreshToken.for_user(self.user1).access_token
        self.user2_token = RefreshToken.for_user(self.user2).access_token

        # Event data for creation tests
        self.new_event_data = {
            'title': 'New Test Event',
            'description': 'Description for new test event',
            'date': (datetime.now() + timedelta(days=30)).isoformat(),
            'location': 'New Test Location'
        }

    def authenticate_user1(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')

    def authenticate_user2(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')

    def test_list_events(self):
        """Test listing all events (no authentication required)"""
        url = reverse('event-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_event_detail(self):
        """Test getting a specific event (no authentication required)"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event 1')

    def test_create_event_authenticated(self):
        """Test creating an event when authenticated"""
        self.authenticate_user1()

        url = reverse('event-list')
        response = self.client.post(url, self.new_event_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Test Event')
        self.assertEqual(response.data['created_by'], self.user1.id)

    def test_create_event_unauthenticated(self):
        """Test creating an event when not authenticated (should fail)"""
        url = reverse('event-list')
        response = self.client.post(url, self.new_event_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Event.objects.count(), 2)  # Count should not change

    def test_update_own_event(self):
        """Test updating an event by its owner"""
        self.authenticate_user1()

        url = reverse('event-detail', args=[self.event1.id])
        update_data = {'title': 'Updated Test Event 1'}
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Test Event 1')

    def test_update_other_user_event(self):
        """Test updating an event by someone who is not the owner (should fail)"""
        self.authenticate_user1()

        url = reverse('event-detail', args=[self.event2.id])
        update_data = {'title': 'Should Not Update'}
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify event wasn't changed
        self.event2.refresh_from_db()
        self.assertEqual(self.event2.title, 'Test Event 2')

    def test_delete_own_event(self):
        """Test deleting an event by its owner"""
        self.authenticate_user1()

        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 1)

    def test_delete_other_user_event(self):
        """Test deleting an event by someone who is not the owner (should fail)"""
        self.authenticate_user1()

        url = reverse('event-detail', args=[self.event2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Event.objects.count(), 2)  # Count should not change

    def test_filter_events_by_date_range(self):
        """Test filtering events by date range"""
        # Create additional events with different dates
        past_event = Event.objects.create(
            title='Past Event',
            description='Event in the past',
            date=datetime.now() - timedelta(days=10),
            location='Past Location',
            created_by=self.user1
        )

        future_event = Event.objects.create(
            title='Far Future Event',
            description='Event in the far future',
            date=datetime.now() + timedelta(days=100),
            location='Future Location',
            created_by=self.user1
        )

        # Calculate filter dates
        min_date = (datetime.now() + timedelta(days=5)).isoformat()
        max_date = (datetime.now() + timedelta(days=25)).isoformat()

        url = reverse('event-list')
        response = self.client.get(f"{url}?min_date={min_date}&max_date={max_date}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Should only include event1 and event2

    def test_filter_events_by_location(self):
        """Test filtering events by location"""
        url = reverse('event-list')
        response = self.client.get(f"{url}?location=Location 1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Event 1')
