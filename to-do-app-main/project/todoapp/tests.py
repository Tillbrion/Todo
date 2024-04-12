from django.test import TestCase

# Create your tests here.
from django.test import TestCase,Client
from django.contrib.auth.models import User
from todoapp.models import Task
from django.urls import reverse

class TaskTestCase(TestCase):
    def setup(self):
        self.client= Client()
        self.user=User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.task =Task.objects.create(
            tittle = 'Test Task',
            discription='this is a test task',
            owner=self.user
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code,302) 
    
        



   