from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from projects.models import Project
from .models import Task, Tag, Comment

User = get_user_model()


class TaskModelTest(TestCase):
    """Test cases for Task model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            project=self.project,
            created_by=self.user
        )

    def test_task_creation(self):
        """Test task creation"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.status, 'todo')
        self.assertEqual(self.task.priority, 'medium')

    def test_task_str(self):
        """Test task string representation"""
        self.assertIn('Test Task', str(self.task))
        self.assertIn('Test Project', str(self.task))

    def test_task_assignees(self):
        """Test assigning users to tasks"""
        assignee = User.objects.create_user(
            email='assignee@example.com',
            username='assignee',
            password='testpass123'
        )
        self.task.assignees.add(assignee)
        self.assertIn(assignee, self.task.assignees.all())


class TagModelTest(TestCase):
    """Test cases for Tag model"""

    def setUp(self):
        self.tag = Tag.objects.create(
            name='Bug',
            color='#ff0000'
        )

    def test_tag_creation(self):
        """Test tag creation"""
        self.assertEqual(self.tag.name, 'Bug')
        self.assertEqual(self.tag.color, '#ff0000')

    def test_tag_str(self):
        """Test tag string representation"""
        self.assertEqual(str(self.tag), 'Bug')


class TaskAPITest(TestCase):
    """Test cases for Task API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.task_data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'project': self.project.id,
            'status': 'todo',
            'priority': 'high'
        }

    def test_task_creation(self):
        """Test creating a task"""
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.created_by, self.user)

    def test_task_list(self):
        """Test listing tasks"""
        Task.objects.create(
            title='Task 1',
            project=self.project,
            created_by=self.user
        )
        Task.objects.create(
            title='Task 2',
            project=self.project,
            created_by=self.user
        )
        response = self.client.get(f'/api/tasks/?project={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_task_filtering_by_status(self):
        """Test filtering tasks by status"""
        Task.objects.create(
            title='Todo Task',
            project=self.project,
            status='todo',
            created_by=self.user
        )
        Task.objects.create(
            title='Done Task',
            project=self.project,
            status='done',
            created_by=self.user
        )
        response = self.client.get(f'/api/tasks/?project={self.project.id}&status=done')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'done')

    def test_task_update(self):
        """Test updating a task"""
        task = Task.objects.create(
            title='Test Task',
            project=self.project,
            created_by=self.user
        )
        update_data = {'status': 'in_progress', 'priority': 'high'}
        response = self.client.patch(f'/api/tasks/{task.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'in_progress')
        self.assertEqual(task.priority, 'high')

    def test_task_delete(self):
        """Test deleting a task"""
        task = Task.objects.create(
            title='Test Task',
            project=self.project,
            created_by=self.user
        )
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class CommentAPITest(TestCase):
    """Test cases for Comment API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            title='Test Project',
            owner=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            project=self.project,
            created_by=self.user
        )

    def test_comment_creation(self):
        """Test creating a comment"""
        comment_data = {
            'content': 'This is a test comment',
            'task': self.task.id
        }
        response = self.client.post('/api/tasks/comments/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get()
        self.assertEqual(comment.content, 'This is a test comment')
        self.assertEqual(comment.author, self.user)

    def test_comment_list(self):
        """Test listing comments"""
        Comment.objects.create(
            content='Comment 1',
            task=self.task,
            author=self.user
        )
        Comment.objects.create(
            content='Comment 2',
            task=self.task,
            author=self.user
        )
        response = self.client.get(f'/api/tasks/comments/?task={self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
