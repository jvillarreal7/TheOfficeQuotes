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
    modified_by = models.PositiveIntegerField(default=None)
    modified_date = models.DateTimeField(default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Quote(AbstractModel):
    """Model that represents a quote from the show."""
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)

    content = models.CharField(max_length=999)


class Actor(AbstractModel):
    """Models that represents any actor from the show."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Character(AbstractModel):
    """Model that represents a character from the show."""
    actor = models.ForeignKey("Actor", on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='characters/', default=None)


class Season(AbstractModel):
    """Model that represents a season of the show."""
    number = models.PositiveIntegerField()


class Episode(AbstractModel):
    """Model that represents an episode of the show."""
    written_by = models.ForeignKey(
        "StaffMember", default=None, on_delete=models.CASCADE, related_name='episodes')
    directed_by = models.ForeignKey(
        "StaffMember", default=None, on_delete=models.CASCADE)

    number = models.PositiveIntegerField()
    air_date = models.DateTimeField(default=None)


class StaffMember(AbstractModel):
    """Model that represents any staff member of the show."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
