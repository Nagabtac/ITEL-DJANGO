from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    motto = models.TextField()

    class Meta:
        db_table = 'students'