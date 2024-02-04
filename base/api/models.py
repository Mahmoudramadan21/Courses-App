from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='media/images', null=True)
    slug = models.SlugField(blank=True, null=True)
    numOfLikes = models.IntegerField(default=0, null=True)
    watches = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Course)
def pre_save_course(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)



class Lecture(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='media/videos',null=True,
            validators=[FileExtensionValidator(
                        allowed_extensions=['MOV',
                        'avi', 'mp4','webm','mkv'])])
    title = models.CharField(max_length=150)
    notes = models.TextField()


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

class View(models.Model):
    _user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    _course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

