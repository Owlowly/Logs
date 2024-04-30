from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

def user_directory_path(instance, filename):
    return f'users/{instance.user.username}/photos/{timezone.now().strftime("%Y/%m/%d")}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    user_follow = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='user_follow',
        blank=True,
        symmetrical=False
    )
    photo = models.ImageField(upload_to=user_directory_path, blank=True, validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'jfif']),
            validate_image,
        ]
    )

    created = models.DateTimeField(auto_now_add=True)
    total_followers = models.PositiveIntegerField(default=0)


    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)




    def __str__(self):
        return f'{self.user}'


    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_followers']),
        ]
        ordering = ['-created']


user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self',
                                                            through=Profile,
                                                            related_name='followers',
                                                            symmetrical=False))


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.recipient} - {self.timestamp}'
