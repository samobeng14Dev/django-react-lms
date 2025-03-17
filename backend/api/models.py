from django.db import models
from userauths.models import User, Profile
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone

# Choices for fields
LANGUAGE = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('French', 'French'),
)

LEVEL = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advance', 'Advance'),
)

TEACHER_STATUS = (
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled'),
    ('Published', 'Published'),
)

PLATFORM_STATUS = (
    ('Review', 'Review'),
    ('Draft', 'Draft'),
    ('Rejected', 'Rejected'),
    ('Published', 'Published'),
)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='course-file',
                             blank=True, default='default.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    X = models.URLField(null=True, blank=True)
    linkedIn = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def student(self):
        return CartOrderItem.objects.filter(teacher=self)

    def courses(self):
        return Course.objects.filter(teacher=self)

    def reviews(self):
        return Course.objects.filter(teacher=self).count()


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='course-file',
                             default='category.jpg', null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "category"
        ordering = ['title']

    def __str__(self):
        return self.title

    def course_count(self):
        return Course.objects.filter(category=self).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course-file', blank=True, null=True)
    image = models.FileField(upload_to='course-file', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(
        choices=LANGUAGE, default='English', max_length=20)
    level = models.CharField(choices=LEVEL, default='Beginner', max_length=20)
    platform_status = models.CharField(
        choices=PLATFORM_STATUS, default='Published', max_length=20)
    teacher_status = models.CharField(
        choices=TEACHER_STATUS, default='Published', max_length=20)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="123456789")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)
