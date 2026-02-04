from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'team_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # In production, use proper password hashing
        user = User.objects.create(**validated_data)
        return user


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'member_count', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return User.objects.filter(team_id=obj.id).count()


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 
                  'calories', 'date', 'notes', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
            return user.username
        except User.DoesNotExist:
            return None


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    class Meta:
        model = Leaderboard
        fields = ['id', 'entity_id', 'entity_type', 'name', 'total_points', 
                  'total_activities', 'total_calories', 'total_duration', 'rank', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'activity_type', 'difficulty', 
                  'duration', 'calories_estimate', 'instructions', 'created_at', 'updated_at']
