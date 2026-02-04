from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )

    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.id)

    def test_user_str_method(self):
        """Test user string representation"""
        expected = f"testuser (test@example.com)"
        self.assertEqual(str(self.user), expected)


class TeamModelTest(TestCase):
    """Test cases for Team model"""

    def setUp(self):
        self.team = Team.objects.create(
            name="Team Alpha",
            description="A great team"
        )

    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, "Team Alpha")
        self.assertEqual(self.team.description, "A great team")
        self.assertTrue(self.team.id)

    def test_team_str_method(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), "Team Alpha")


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.activity = Activity.objects.create(
            user_id=self.user.id,
            activity_type="running",
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now(),
            notes="Morning run"
        )

    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.activity_type, "running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)
        self.assertTrue(self.activity.id)

    def test_activity_str_method(self):
        """Test activity string representation"""
        expected = "running - 30 mins"
        self.assertEqual(str(self.activity), expected)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""

    def setUp(self):
        self.leaderboard_entry = Leaderboard.objects.create(
            entity_id=1,
            entity_type="user",
            name="TestUser",
            total_points=1000,
            total_activities=10,
            total_calories=5000,
            total_duration=300,
            rank=1
        )

    def test_leaderboard_creation(self):
        """Test leaderboard entry is created correctly"""
        self.assertEqual(self.leaderboard_entry.entity_type, "user")
        self.assertEqual(self.leaderboard_entry.total_points, 1000)
        self.assertEqual(self.leaderboard_entry.rank, 1)

    def test_leaderboard_str_method(self):
        """Test leaderboard string representation"""
        expected = "TestUser - Rank #1"
        self.assertEqual(str(self.leaderboard_entry), expected)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""

    def setUp(self):
        self.workout = Workout.objects.create(
            title="Morning Cardio",
            description="A great way to start the day",
            activity_type="running",
            difficulty="intermediate",
            duration=45,
            calories_estimate=400,
            instructions="Warm up, run, cool down"
        )

    def test_workout_creation(self):
        """Test workout is created correctly"""
        self.assertEqual(self.workout.title, "Morning Cardio")
        self.assertEqual(self.workout.difficulty, "intermediate")
        self.assertEqual(self.workout.duration, 45)

    def test_workout_str_method(self):
        """Test workout string representation"""
        expected = "Morning Cardio (intermediate)"
        self.assertEqual(str(self.workout), expected)


class APITestCases(APITestCase):
    """Test cases for API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            email="api@example.com",
            username="apiuser",
            password="testpass"
        )
        self.team = Team.objects.create(
            name="API Team",
            description="Test team"
        )

    def test_api_root(self):
        """Test API root endpoint"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_user_list(self):
        """Test user list endpoint"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_user_detail(self):
        """Test user detail endpoint"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apiuser')

    def test_team_list(self):
        """Test team list endpoint"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_team_detail(self):
        """Test team detail endpoint"""
        url = reverse('team-detail', args=[self.team.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Team')

    def test_activity_list(self):
        """Test activity list endpoint"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leaderboard_list(self):
        """Test leaderboard list endpoint"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workout_list(self):
        """Test workout list endpoint"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        """Test creating a new user"""
        url = reverse('user-list')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_team_create(self):
        """Test creating a new team"""
        url = reverse('team-list')
        data = {
            'name': 'New Team',
            'description': 'A new test team'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_activity_create(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        data = {
            'user_id': self.user.id,
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat(),
            'notes': 'Test run'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
