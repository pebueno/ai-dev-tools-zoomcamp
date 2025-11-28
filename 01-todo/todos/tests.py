from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=date.today() + timedelta(days=7)
        )

    def test_todo_creation(self):
        """Test that a todo is created with correct attributes"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertEqual(self.todo.resolved, False)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_str_method(self):
        """Test the string representation of a todo"""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_default_resolved_is_false(self):
        """Test that resolved defaults to False"""
        new_todo = Todo.objects.create(title="Another Todo")
        self.assertFalse(new_todo.resolved)

    def test_todo_optional_fields(self):
        """Test that description and due_date are optional"""
        todo_minimal = Todo.objects.create(title="Minimal Todo")
        self.assertEqual(todo_minimal.description, "")
        self.assertIsNone(todo_minimal.due_date)

    def test_todo_ordering(self):
        """Test that todos are ordered by creation date (newest first)"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todo3 = Todo.objects.create(title="Third")

        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo3)
        self.assertEqual(todos[1], todo2)
        self.assertEqual(todos[2], todo1)


class TodoListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo_list')

    def test_todo_list_view_status_code(self):
        """Test that the list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_todo_list_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_list.html')

    def test_todo_list_view_displays_todos(self):
        """Test that todos are displayed in the list"""
        Todo.objects.create(title="Todo 1")
        Todo.objects.create(title="Todo 2")

        response = self.client.get(self.url)
        self.assertContains(response, "Todo 1")
        self.assertContains(response, "Todo 2")

    def test_todo_list_empty_state(self):
        """Test that empty state is displayed when no todos exist"""
        response = self.client.get(self.url)
        self.assertContains(response, "No todos yet!")


class TodoCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo_create')

    def test_todo_create_view_get(self):
        """Test that the create view displays the form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_todo_create_view_post_valid(self):
        """Test creating a todo with valid data"""
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New Todo')
        self.assertEqual(todo.description, 'New Description')

    def test_todo_create_view_post_minimal(self):
        """Test creating a todo with only required fields"""
        data = {'title': 'Minimal Todo'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

    def test_todo_create_view_post_invalid(self):
        """Test creating a todo without required title"""
        data = {'description': 'No title'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), 0)
        self.assertContains(response, 'Title is required!')


class TodoEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original Description"
        )
        self.url = reverse('todo_edit', kwargs={'pk': self.todo.pk})

    def test_todo_edit_view_get(self):
        """Test that the edit view displays the form with existing data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, "Original Title")

    def test_todo_edit_view_post_valid(self):
        """Test updating a todo with valid data"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'due_date': date.today().strftime('%Y-%m-%d')
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')

    def test_todo_edit_view_post_invalid(self):
        """Test updating a todo without title"""
        data = {'title': '', 'description': 'Updated'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title is required!')

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Original Title')

    def test_todo_edit_view_404(self):
        """Test that editing non-existent todo returns 404"""
        url = reverse('todo_edit', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="To Delete")
        self.url = reverse('todo_delete', kwargs={'pk': self.todo.pk})

    def test_todo_delete_view_get(self):
        """Test that the delete confirmation page is displayed"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, "To Delete")

    def test_todo_delete_view_post(self):
        """Test that posting to delete view removes the todo"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_delete_view_404(self):
        """Test that deleting non-existent todo returns 404"""
        url = reverse('todo_delete', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleResolvedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Toggle Me", resolved=False)
        self.url = reverse('todo_toggle_resolved', kwargs={'pk': self.todo.pk})

    def test_todo_toggle_resolved_to_true(self):
        """Test toggling a todo from unresolved to resolved"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)

    def test_todo_toggle_resolved_to_false(self):
        """Test toggling a todo from resolved to unresolved"""
        self.todo.resolved = True
        self.todo.save()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        self.todo.refresh_from_db()
        self.assertFalse(self.todo.resolved)

    def test_todo_toggle_multiple_times(self):
        """Test toggling a todo multiple times"""
        self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)

        self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.resolved)

        self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)

    def test_todo_toggle_404(self):
        """Test that toggling non-existent todo returns 404"""
        url = reverse('todo_toggle_resolved', kwargs={'pk': 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class TodoIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_complete_todo_workflow(self):
        """Test creating, editing, toggling, and deleting a todo"""
        # Create a todo
        create_url = reverse('todo_create')
        create_data = {
            'title': 'Integration Test Todo',
            'description': 'Testing complete workflow',
            'due_date': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d')
        }
        self.client.post(create_url, create_data)

        todo = Todo.objects.first()
        self.assertIsNotNone(todo)
        self.assertEqual(todo.title, 'Integration Test Todo')
        self.assertFalse(todo.resolved)

        # Edit the todo
        edit_url = reverse('todo_edit', kwargs={'pk': todo.pk})
        edit_data = {
            'title': 'Updated Integration Test',
            'description': 'Updated description',
            'due_date': date.today().strftime('%Y-%m-%d')
        }
        self.client.post(edit_url, edit_data)

        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Integration Test')

        # Toggle resolved status
        toggle_url = reverse('todo_toggle_resolved', kwargs={'pk': todo.pk})
        self.client.post(toggle_url)

        todo.refresh_from_db()
        self.assertTrue(todo.resolved)

        # Delete the todo
        delete_url = reverse('todo_delete', kwargs={'pk': todo.pk})
        self.client.post(delete_url)

        self.assertEqual(Todo.objects.count(), 0)

    def test_multiple_todos_management(self):
        """Test managing multiple todos simultaneously"""
        # Create multiple todos
        todos_data = [
            {'title': 'Todo 1', 'description': 'First'},
            {'title': 'Todo 2', 'description': 'Second'},
            {'title': 'Todo 3', 'description': 'Third'},
        ]

        create_url = reverse('todo_create')
        for data in todos_data:
            self.client.post(create_url, data)

        self.assertEqual(Todo.objects.count(), 3)

        # Mark some as resolved
        todos = Todo.objects.all()
        toggle_url = reverse('todo_toggle_resolved', kwargs={'pk': todos[0].pk})
        self.client.post(toggle_url)

        resolved_count = Todo.objects.filter(resolved=True).count()
        unresolved_count = Todo.objects.filter(resolved=False).count()

        self.assertEqual(resolved_count, 1)
        self.assertEqual(unresolved_count, 2)
