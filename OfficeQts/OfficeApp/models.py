from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Flexible user model that may have attributes other than the default if needed."""
    pass


class AbstractModel(models.Model):
    """General attributes that consequent models will have as well."""
    created_by = models.PositiveIntegerField(default=None)
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.PositiveIntegerField(
        default=None, blank=True, null=True)
    modified_date = models.DateTimeField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Quote(AbstractModel):
    """Model that represents a quote from the show."""
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)

    content = models.CharField(max_length=999)

    def __str__(self):
        return self.character.first_name + " " + self.character.last_name + ": " + self.content


class Actor(AbstractModel):
    """Models that represents any actor from the show."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Character(AbstractModel):
    """Model that represents a character from the show."""
    actor = models.ForeignKey("Actor", on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='characters/', default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Season(AbstractModel):
    """Model that represents a season of the show."""
    number = models.PositiveIntegerField()

    def __str__(self):
        return "Season " + str(self.number)


class Episode(AbstractModel):
    """Model that represents an episode of the show."""
    directed_by = models.ForeignKey(
        "StaffMember", default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='episodes_d')
    written_by = models.ForeignKey(
        "StaffMember", default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='episodes_w')
    season = models.ForeignKey("Season", on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    air_date = models.DateField(default=None)
    running_time = models.PositiveIntegerField()

    def __str__(self):
        return "Season " + str(self.season.number) + " / " + "Episode " + str(self.number) + ": " + self.name


class StaffMember(AbstractModel):
    """Model that represents any staff member of the show."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name
