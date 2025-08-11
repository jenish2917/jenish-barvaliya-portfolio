from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Contact, Project


class ContactAPITestCase(APITestCase):
    def test_create_contact(self):
        """Test creating a new contact submission"""
        url = reverse('contact-list')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Test User')


class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            technologies=['Python', 'Django'],
            status='completed',
            is_featured=True
        )
    
    def test_get_projects(self):
        """Test retrieving projects"""
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Project')
