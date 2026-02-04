from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ('id', 'username', 'email', 'team_id', 'created_at')
    list_filter = ('team_id', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Team', {
            'fields': ('team_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ('id', 'name', 'created_at', 'member_count')
    search_fields = ('name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def member_count(self, obj):
        """Display member count for team"""
        return User.objects.filter(team_id=obj.id).count()
    member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ('id', 'user_id', 'activity_type', 'duration', 'calories', 'date', 'created_at')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user_id', 'notes')
    ordering = ('-date',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Activity Information', {
            'fields': ('user_id', 'activity_type', 'date')
        }),
        ('Metrics', {
            'fields': ('duration', 'distance', 'calories')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ('rank', 'name', 'entity_type', 'total_points', 'total_activities', 'total_calories', 'total_duration')
    list_filter = ('entity_type', 'rank')
    search_fields = ('name',)
    ordering = ('rank',)
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('Entity Information', {
            'fields': ('entity_id', 'entity_type', 'name')
        }),
        ('Statistics', {
            'fields': ('total_points', 'total_activities', 'total_calories', 'total_duration', 'rank')
        }),
        ('Timestamp', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ('id', 'title', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'created_at')
    list_filter = ('activity_type', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'instructions')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Workout Information', {
            'fields': ('title', 'description', 'activity_type', 'difficulty')
        }),
        ('Estimates', {
            'fields': ('duration', 'calories_estimate')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
