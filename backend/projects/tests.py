from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project

User = get_user_model()


class ProjectModelTest(TestCase):
    """Test cases for Project model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            username='owner',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.user
        )

    def test_project_creation(self):
        """Test project creation"""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.owner, self.user)
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_members(self):
        """Test adding members to project"""
        member = User.objects.create_user(
            email='member@example.com',
            username='member',
            password='testpass123'
        )
        self.project.members.add(member)
        self.assertIn(member, self.project.members.all())


class ProjectAPITest(TestCase):
    """Test cases for Project API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project_data = {
            'title': 'New Project',
            'description': 'New Project Description'
        }

    def test_project_creation(self):
        """Test creating a project"""
        response = self.client.post('/api/projects/', self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().owner, self.user)

    def test_project_list(self):
        """Test listing projects"""
        Project.objects.create(
            title='Project 1',
            owner=self.user
        )
        Project.objects.create(
            title='Project 2',
            owner=self.user
        )
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_project_retrieve(self):
        """Test retrieving a project"""
        project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        response = self.client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Project')

    def test_project_update(self):
        """Test updating a project"""
        project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        update_data = {'title': 'Updated Project'}
        response = self.client.patch(f'/api/projects/{project.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.title, 'Updated Project')

    def test_project_delete(self):
        """Test deleting a project"""
        project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        response = self.client.delete(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_project_access_denied_for_non_member(self):
        """Test that non-members cannot access projects"""
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        project = Project.objects.create(
            title='Private Project',
            owner=other_user
        )
        response = self.client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
