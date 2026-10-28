from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100, default='online course')
    description = models.CharField(max_length=500)
    total_enrollment = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    order = models.IntegerField(default=0)

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_point = models.IntegerField(default=1)
    grade = models.IntegerField(default=5)  # Required grade field

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_correct = True
        # Get correct choices for this question
        correct_choices = self.choice_set.filter(is_correct=True)
        correct_ids = set(correct_choices.values_list('id', flat=True))
        
        if set(selected_ids) == correct_ids:
            all_correct = True
        else:
            all_correct = False
        return all_correct

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, default='audit')

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    
    def __str__(self):
        return str(self.id)
