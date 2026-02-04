from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes on Earth working together.'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League united! Protecting the world from threats.'
        )

        # Create Users - Marvel Heroes
        self.stdout.write('Creating Marvel heroes...')
        marvel_users = [
            {'email': 'tony.stark@marvel.com', 'username': 'Iron Man', 'password': 'jarvis123'},
            {'email': 'steve.rogers@marvel.com', 'username': 'Captain America', 'password': 'shield456'},
            {'email': 'thor.odinson@marvel.com', 'username': 'Thor', 'password': 'mjolnir789'},
            {'email': 'bruce.banner@marvel.com', 'username': 'Hulk', 'password': 'smash321'},
            {'email': 'natasha.romanoff@marvel.com', 'username': 'Black Widow', 'password': 'widow654'},
            {'email': 'peter.parker@marvel.com', 'username': 'Spider-Man', 'password': 'webslinger'},
        ]

        for user_data in marvel_users:
            User.objects.create(team_id=team_marvel.id, **user_data)

        # Create Users - DC Heroes
        self.stdout.write('Creating DC heroes...')
        dc_users = [
            {'email': 'bruce.wayne@dc.com', 'username': 'Batman', 'password': 'gotham123'},
            {'email': 'clark.kent@dc.com', 'username': 'Superman', 'password': 'krypton456'},
            {'email': 'diana.prince@dc.com', 'username': 'Wonder Woman', 'password': 'amazon789'},
            {'email': 'barry.allen@dc.com', 'username': 'The Flash', 'password': 'speed321'},
            {'email': 'arthur.curry@dc.com', 'username': 'Aquaman', 'password': 'ocean654'},
            {'email': 'hal.jordan@dc.com', 'username': 'Green Lantern', 'password': 'willpower'},
        ]

        for user_data in dc_users:
            User.objects.create(team_id=team_dc.id, **user_data)

        # Create Activities
        self.stdout.write('Creating activities...')
        all_users = User.objects.all()
        activity_types = ['running', 'cycling', 'swimming', 'walking', 'weightlifting', 'yoga']
        
        for user in all_users:
            # Create 5-10 random activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(1.0, 20.0), 2) if activity_type in ['running', 'cycling', 'swimming', 'walking'] else None
                calories = random.randint(100, 800)
                days_ago = random.randint(0, 30)
                date = timezone.now() - timedelta(days=days_ago)
                
                notes_options = [
                    'Great workout!',
                    'Feeling strong today',
                    'Good progress',
                    'Challenging but rewarding',
                    'New personal best!',
                    '',
                ]
                
                Activity.objects.create(
                    user_id=user.id,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=date,
                    notes=random.choice(notes_options)
                )

        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts_data = [
            {
                'title': 'Morning Power Run',
                'description': 'Start your day with an energizing run',
                'activity_type': 'running',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 300,
                'instructions': '1. Warm up with 5 min walk\n2. Run at steady pace for 20 min\n3. Cool down with 5 min walk\n4. Stretch for 5 minutes'
            },
            {
                'title': 'Interval Speed Training',
                'description': 'High-intensity interval training for runners',
                'activity_type': 'running',
                'difficulty': 'advanced',
                'duration': 45,
                'calories_estimate': 500,
                'instructions': '1. Warm up 10 min\n2. Sprint 1 min, jog 2 min (repeat 8x)\n3. Cool down 10 min\n4. Stretch'
            },
            {
                'title': 'Beginner Yoga Flow',
                'description': 'Gentle yoga session for flexibility and relaxation',
                'activity_type': 'yoga',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 120,
                'instructions': '1. Mountain pose\n2. Sun salutations (5x)\n3. Warrior poses\n4. Tree pose\n5. Savasana'
            },
            {
                'title': 'Strength Builder',
                'description': 'Full body weightlifting routine',
                'activity_type': 'weightlifting',
                'difficulty': 'intermediate',
                'duration': 60,
                'calories_estimate': 400,
                'instructions': '1. Squats 3x10\n2. Bench press 3x10\n3. Deadlifts 3x8\n4. Shoulder press 3x10\n5. Cool down'
            },
            {
                'title': 'Cycling Adventure',
                'description': 'Scenic outdoor cycling route',
                'activity_type': 'cycling',
                'difficulty': 'intermediate',
                'duration': 60,
                'calories_estimate': 450,
                'instructions': '1. Check bike and gear\n2. Warm up 10 min easy pace\n3. Ride 40 min moderate pace\n4. Cool down 10 min'
            },
            {
                'title': 'Pool Workout',
                'description': 'Comprehensive swimming workout',
                'activity_type': 'swimming',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 400,
                'instructions': '1. Warm up 200m easy\n2. 10x100m freestyle\n3. 8x50m kick drills\n4. Cool down 200m'
            },
            {
                'title': 'Power Yoga',
                'description': 'Advanced yoga for strength and flexibility',
                'activity_type': 'yoga',
                'difficulty': 'advanced',
                'duration': 60,
                'calories_estimate': 250,
                'instructions': '1. Dynamic sun salutations\n2. Arm balances\n3. Advanced poses\n4. Core work\n5. Deep stretching'
            },
            {
                'title': 'Easy Walk',
                'description': 'Relaxing walk for beginners',
                'activity_type': 'walking',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 150,
                'instructions': '1. Walk at comfortable pace\n2. Focus on posture\n3. Breathe deeply\n4. Enjoy nature'
            },
        ]

        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        # Calculate and populate leaderboard
        self.stdout.write('Calculating leaderboard...')
        from django.db.models import Sum, Count
        
        # User leaderboard
        user_stats = []
        for user in all_users:
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

        # Team leaderboard
        teams = [team_marvel, team_dc]
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

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams created: {Team.objects.count()}')
        self.stdout.write(f'Users created: {User.objects.count()}')
        self.stdout.write(f'Activities created: {Activity.objects.count()}')
        self.stdout.write(f'Workouts created: {Workout.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*40))
