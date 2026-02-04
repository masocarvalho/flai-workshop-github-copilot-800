from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Sum, Count
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint showing available endpoints"""
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'leaderboard': reverse('leaderboard-list', request=request, format=format),
        'workouts': reverse('workout-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=user.id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=user.id)
        stats = activities.aggregate(
            total_activities=Count('id'),
            total_duration=Sum('duration'),
            total_calories=Sum('calories'),
            total_distance=Sum('distance')
        )
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        users = User.objects.filter(team_id=team.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific team"""
        team = self.get_object()
        user_ids = User.objects.filter(team_id=team.id).values_list('id', flat=True)
        activities = Activity.objects.filter(user_id__in=user_ids)
        stats = activities.aggregate(
            total_activities=Count('id'),
            total_duration=Sum('duration'),
            total_calories=Sum('calories'),
            total_distance=Sum('distance')
        )
        stats['member_count'] = len(user_ids)
        return Response(stats)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """Filter activities by user_id if provided"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        """Filter leaderboard by entity_type if provided"""
        queryset = Leaderboard.objects.all()
        entity_type = self.request.query_params.get('type', None)
        if entity_type is not None:
            queryset = queryset.filter(entity_type=entity_type)
        return queryset

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Recalculate leaderboard rankings"""
        # Clear existing leaderboard
        Leaderboard.objects.all().delete()

        # Calculate user rankings
        users = User.objects.all()
        user_stats = []
        for user in users:
            activities = Activity.objects.filter(user_id=user.id)
            stats = activities.aggregate(
                total_activities=Count('id'),
                total_duration=Sum('duration'),
                total_calories=Sum('calories')
            )
            total_points = (stats['total_activities'] or 0) * 10 + (stats['total_calories'] or 0)
            user_stats.append({
                'entity_id': user.id,
                'entity_type': 'user',
                'name': user.username,
                'total_points': total_points,
                'total_activities': stats['total_activities'] or 0,
                'total_calories': stats['total_calories'] or 0,
                'total_duration': stats['total_duration'] or 0,
            })

        # Sort by points and assign ranks
        user_stats.sort(key=lambda x: x['total_points'], reverse=True)
        for rank, stat in enumerate(user_stats, 1):
            stat['rank'] = rank
            Leaderboard.objects.create(**stat)

        # Calculate team rankings
        teams = Team.objects.all()
        team_stats = []
        for team in teams:
            user_ids = User.objects.filter(team_id=team.id).values_list('id', flat=True)
            activities = Activity.objects.filter(user_id__in=user_ids)
            stats = activities.aggregate(
                total_activities=Count('id'),
                total_duration=Sum('duration'),
                total_calories=Sum('calories')
            )
            total_points = (stats['total_activities'] or 0) * 10 + (stats['total_calories'] or 0)
            team_stats.append({
                'entity_id': team.id,
                'entity_type': 'team',
                'name': team.name,
                'total_points': total_points,
                'total_activities': stats['total_activities'] or 0,
                'total_calories': stats['total_calories'] or 0,
                'total_duration': stats['total_duration'] or 0,
            })

        # Sort by points and assign ranks
        team_stats.sort(key=lambda x: x['total_points'], reverse=True)
        for rank, stat in enumerate(team_stats, 1):
            stat['rank'] = rank
            Leaderboard.objects.create(**stat)

        return Response({'message': 'Leaderboard refreshed successfully'})


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        """Filter workouts by difficulty or activity_type if provided"""
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if difficulty is not None:
            queryset = queryset.filter(difficulty=difficulty)
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def suggest(self, request):
        """Get personalized workout suggestions"""
        difficulty = request.query_params.get('difficulty', 'beginner')
        workouts = Workout.objects.filter(difficulty=difficulty)[:5]
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
