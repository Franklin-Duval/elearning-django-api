from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Classe(models.Model):
    """
        Modelizes a highschool `class`
    """
    name = models.CharField(max_length=20, unique=True, null=False)
    abbrev = models.CharField(max_length=5, unique=True, null=False)
    number_courses = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def increment_course(self):
        self.number_courses = self.number_courses + 1
        self.save()


class Subject(models.Model):
    """
        Modelizes a `subject`
    """
    name = models.CharField(max_length=20, null=False, unique=True)
    number_courses = models.IntegerField(default=0)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    def increment_course(self):
        self.number_courses = self.number_courses + 1
        self.save()


class Users(User):
    """
        Extends Django User model to enrich default model
    """
    TYPE = (
        ('Elève', 'Elève'),
        ('Enseignant', 'Enseignant')
    )
    telephone = models.CharField(max_length=20, null=False, unique=True)
    type = models.CharField(max_length=15, choices=TYPE)
    favoris = models.TextField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    """
        Modelizes a Course (Chapter)
    """
    title = models.CharField(max_length=50, null=False)
    detailImage = models.ImageField(null=True,  upload_to="images/")
    video = models.FileField(null=True, upload_to="videos/")
    content = models.FileField(null=True, upload_to="contents/")
    rating = models.IntegerField(null=False, default=0)
    keywords = models.TextField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    validated = models.BooleanField(default=False)
    number_users = models.IntegerField(null=False, default=0)
    number_comments = models.IntegerField(null=False, default=0)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title + " " + self.level.name

    def increment_comment(self):
        self.number_comments = self.number_comments + 1
        self.save()

    def increment_user(self):
        self.number_users = self.number_users + 1
        self.save()


class Exam(models.Model):
    """
        Modelizes an Exam related to a Course. It is answered after a course is followed
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to="exams/")
    correction = models.FileField(upload_to="corrections/")

class Comments(models.Model):
    """
        Modelizes comments related to a course
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    comment = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + str(self.date)


class Inscription(models.Model):
    """
        Modelizes users who have subscribed to a course
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.title + " " + self.user.username + " " + str(self.date)