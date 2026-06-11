from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Lesson, Question, Choice, Submission, Enrollment


def get_enrollment(user, course_id):
    """Helper: return enrollment or None."""
    try:
        return Enrollment.objects.get(user=user, course_id=course_id)
    except Enrollment.DoesNotExist:
        return None


@login_required
def submit(request, course_id):
    """
    Handle exam submission.
    Collects selected choice IDs from POST, creates a Submission,
    attaches the choices, then redirects to show_exam_result.
    """
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_enrollment(request.user, course_id)

    if enrollment is None:
        return redirect(reverse('onlinecourse:index'))

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)

        # Collect all submitted choice ids from POST data
        # Each checkbox is named "choice" with value = choice_id
        submitted_choice_ids = request.POST.getlist('choice')
        for choice_id in submitted_choice_ids:
            try:
                choice = Choice.objects.get(pk=int(choice_id))
                submission.choices.add(choice)
            except (Choice.DoesNotExist, ValueError):
                pass

        submission.save()
        return HttpResponseRedirect(
            reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
        )

    # GET not allowed for submit — redirect back to course
    return redirect(reverse('onlinecourse:course_details', args=(course_id,)))


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Display exam results.
    Calculates total score by comparing submitted choices against correct answers.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Retrieve all questions for this course (across all lessons)
    questions = Question.objects.filter(lesson__course=course)

    total_score = 0.0
    total_possible = 0.0
    results = []

    submitted_choices = submission.choices.all()
    submitted_choice_ids = set(submitted_choices.values_list('id', flat=True))

    for question in questions:
        correct_choices = set(
            question.choices.filter(is_correct=True).values_list('id', flat=True)
        )
        selected_for_q = set(
            question.choices.filter(id__in=submitted_choice_ids).values_list('id', flat=True)
        )

        # Full credit only if selected set exactly matches correct set
        is_correct = (selected_for_q == correct_choices) and len(correct_choices) > 0
        if is_correct:
            total_score += question.grade

        total_possible += question.grade

        results.append({
            'question': question,
            'selected_choices': selected_for_q,
            'correct_choices': correct_choices,
            'is_correct': is_correct,
        })

    context = {
        'course': course,
        'submission': submission,
        'results': results,
        'total_score': total_score,
        'total_possible': total_possible,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
