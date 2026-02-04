from django.db import models
from django.core.validators import EmailValidator


class User(models.Model):
    """User model for OctoFit Tracker"""
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    team_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Team(models.Model):
    """Team model for OctoFit Tracker"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking user workouts"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('weightlifting', 'Weightlifting'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]

    user_id = models.IntegerField()
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(null=True, blank=True, help_text="Distance in kilometers")
    calories = models.IntegerField(help_text="Calories burned")
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user_id', '-date']),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    """Leaderboard model for ranking users and teams"""
    RANKING_TYPES = [
        ('user', 'User'),
        ('team', 'Team'),
    ]

    entity_id = models.IntegerField(help_text="User ID or Team ID")
    entity_type = models.CharField(max_length=10, choices=RANKING_TYPES)
    name = models.CharField(max_length=100)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0, help_text="Total duration in minutes")
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        indexes = [
            models.Index(fields=['entity_type', 'rank']),
        ]

    def __str__(self):
        return f"{self.name} - Rank #{self.rank}"


class Workout(models.Model):
    """Workout suggestion model"""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.IntegerField(help_text="Estimated duration in minutes")
    calories_estimate = models.IntegerField(help_text="Estimated calories burned")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        indexes = [
            models.Index(fields=['activity_type', 'difficulty']),
        ]

    def __str__(self):
        return f"{self.title} ({self.difficulty})"
