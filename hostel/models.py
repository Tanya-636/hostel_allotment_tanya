from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('VJNT', 'VJNT'),
    ]

    registration_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Increased max_length
    cet_percentile = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  # To display student names in Django admin or dropdowns


class Room(models.Model):
    building = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    total_capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)

    def __str__(self):
        return f'Room {self.room_number} ({self.current_capacity}/{self.total_capacity} filled)'  # Display room details


class Allotment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocation_date = models.DateTimeField(auto_now_add=True)

    # Ensure that a student can only have one room allotted
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student'], name='unique_student_allotment')
        ]

    def __str__(self):
        return f'{self.student.name} -> {self.room.room_number}'  # Allotment detail display
