from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Quiz, Question, Choice, QuizResult
from .forms import QuizForm, QuestionFormSet, ChoiceFormSet

def index(request):
    return render(
        request,
        'core/index.html',
    )

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(
        request,
        'core/quiz_list.html',
        {'quizzes': quizzes}
    )

@login_required
def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return render(
        request,
        'core/quiz_detail.html',
        {'quiz': quiz}
    )

@login_required
def quiz_submit(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    total_questions = quiz.questions.count()
    correct_answers = 0

    for question in quiz.questions.all():
        selected_choice_id = request.POST.get(f'question_{question.id}')
        if selected_choice_id:
            selected_choice = Choice.objects.get(id=selected_choice_id)
            if selected_choice.is_correct:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    QuizResult.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        correct_answers=correct_answers,
        total_questions=total_questions
    )

    return render(
        request,
        'core/quiz_submit.html',
        {
            'quiz': quiz,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score
        }
    )

@login_required
def quiz_create(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='q')
        if quiz_form.is_valid() and question_formset.is_valid():
            with transaction.atomic():
                quiz = quiz_form.save(commit=False)
                quiz.author = request.user
                quiz.save()
                for q_index, q_form in enumerate(question_formset.forms):
                    if not q_form.cleaned_data or q_form.cleaned_data.get('DELETE'):
                        continue
                    question = Question.objects.create(
                        quiz=quiz,
                        text=q_form.cleaned_data['text']
                    )
                    c_index = 0
                    while True:
                        text_key = f'c-{q_index}-{c_index}-text'
                        if text_key not in request.POST:
                            break
                        choice_text = request.POST.get(text_key, '').strip()
                        if choice_text:
                            is_correct = request.POST.get(f'c-{q_index}-{c_index}-is_correct') == 'on'
                            Choice.objects.create(
                                question=question,
                                text=choice_text,
                                is_correct=is_correct
                            )
                        c_index += 1
            return redirect('core:quiz_detail', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix='q')

    return render(
        request,
        'core/quiz_create.html',
        {
            'quiz_form': quiz_form,
            'question_formset': question_formset,
        }
    )

@login_required
def user_quizzes(request):
    quizzes = Quiz.objects.filter(author=request.user)
    return render(
        request,
        'core/user_quizzes.html',
        {'quizzes': quizzes}
    )

@login_required
def quiz_confirm_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.author != request.user:
        return HttpResponseForbidden("Not allowed")
    return render(request, 'core/quiz_confirm_delete.html', {'quiz': quiz})

@require_POST
@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.author != request.user:
        return HttpResponseForbidden("Not allowed")
    quiz.delete()
    return HttpResponse("")

@login_required
def user_quizzes_results(request):
    if not request.user.is_authenticated:
        return redirect('login')
    results = QuizResult.objects.filter(user=request.user).select_related('quiz')
    return render(
        request,
        'core/user_quizzes_results.html',
        {'results': results}
    )