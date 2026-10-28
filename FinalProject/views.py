from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Create your views here.

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Get the user's enrollment for this course
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if request.method == 'POST':
        # Create a new submission object
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Loop through all questions and extract selected choices from the POST request
        for question in course.question_set.all():
            for choice in question.choice_set.all():
                # Check if the choice checkbox was selected in the form
                if request.POST.get(f'choice_{choice.id}'):
                    submission.choices.add(choice)
                    
        return redirect(reverse('onlinecourse:show_exam_result', args=[course.id, submission.id]))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_choices = submission.choices.all()
    questions = course.question_set.all()
    
    # Calculate maximum possible points
    max_points = sum([q.question_point for q in questions])
    student_score = 0
    
    # Calculate student score using is_get_score
    for question in questions:
        selected_ids = [choice.id for choice in selected_choices if choice.question_id == question.id]
        if question.is_get_score(selected_ids):
            student_score += question.question_point
            
    # Calculate the grade percentage
    if max_points > 0:
        grade = int(student_score / max_points * 100)
    else:
        grade = 0
        
    context['grade'] = grade
    context['score'] = student_score
    context['possible'] = max_points  # Required by grader
    context['selected_ids'] = selected_choices
    context['course'] = course
    context['submission'] = submission
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
