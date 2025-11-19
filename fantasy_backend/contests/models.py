from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, blank=True, null=True)
    day = models.CharField(max_length=2, blank=True, null=True)
    month = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Contest(models.Model):
    name = models.CharField(max_length=100, default="User")  # Default name
    sport = models.CharField(
        max_length=50,
        choices=[('Football', 'Football'), ('Cricket', 'Cricket'), ('Basketball', 'Basketball')],
        default='Football'
    )
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Avoid NULL issue
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=now)  # Default to current time
    league_code = models.CharField(max_length=12, unique=True, default="XYZ")  # Default league code
    league_type = models.CharField(
        max_length=10,
        choices=[('Public', 'Public'), ('Private', 'Private')],
        default='Public'
    )
    users = models.ManyToManyField('auth.User', related_name='leagues', blank=True)  # Avoid NULL issue
    gameweek = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def update_prize_pool(self):
        """Update the prize pool based on the number of users."""
        self.prize_pool = self.entry_fee * self.users.count()
        self.save()

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default user
    player_id = models.IntegerField(default=0)  # External ID from API
    name = models.CharField(max_length=100, default="User")  # Default name
    formation_name = models.CharField(max_length=100, default="3-3-3")  # Default formation
    position_coordinates = models.JSONField(default=dict)
    position = models.CharField(max_length=50, default="DEF")  # Default position
    team = models.CharField(max_length=100, default="Team")  # Default real-life football team
    kickoff = models.CharField(max_length=100, default="2025-02-25T19:30:00Z")
    score = models.IntegerField(default=0)
    gameweek = models.IntegerField(default=0)
    image_url = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default user
    players = models.ManyToManyField(Player, related_name="teams", blank=True)  # Avoid NULL issue
    name = models.CharField(max_length=20, default="User")  # Default name
    favorite_club = models.CharField(max_length=50, default="City")  # Default favorite club
    score = models.IntegerField(default=0)
    captain = models.ForeignKey(Player, related_name='captain_team', on_delete=models.SET_NULL, null=True, blank=True)
    vice_captain = models.ForeignKey(Player, related_name='vice_captain_team', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Team: {self.name}"

class CaptainViceCaptainHistory(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    captain = models.ForeignKey(Player, related_name="captain_history", on_delete=models.SET_NULL, null=True, blank=True)
    vice_captain = models.ForeignKey(Player, related_name="vice_captain_history", on_delete=models.SET_NULL, null=True, blank=True)
    gameweek = models.IntegerField()
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        captain_name = self.captain.name if self.captain else "No Captain"
        vice_captain_name = self.vice_captain.name if self.vice_captain else "No Vice-Captain"
        return f"Gameweek {self.gameweek}: {self.team.name} Captain: {captain_name} | Vice-Captain: {vice_captain_name}"

class MpesaPayment(models.Model):
    checkout_request_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    raw = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)