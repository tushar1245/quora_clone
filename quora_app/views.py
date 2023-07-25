from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Like
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm 

def base(request):
    return render(request, 'base.html')

def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def post_question(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST['text']
        question = Question.objects.create(user=user, text=text)
        return redirect('home')
    return render(request, 'quora_app/post_question.html')

@login_required
def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question=question)
    for answer in answers:
        answer.like_count = answer.like_set.count()
    
    return render(request, 'question_detail.html', {'question': question, 'answers': answers})

@login_required
def post_answer(request, question_id):
    if request.method == 'POST':
        user = request.user
        question = Question.objects.get(pk=question_id)
        text = request.POST['text']
        answer = Answer.objects.create(user=user, question=question, text=text)
        return redirect('question_detail', question_id=question_id)
    return render(request, 'post_answer.html', {'question_id': question_id})

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # Check if the user has already liked the answer
    if not Like.objects.filter(user=request.user, answer=answer).exists():
        Like.objects.create(user=request.user, answer=answer)

    return redirect('question_detail', question_id=answer.question.id)



@login_required
def logout_user(request):
    logout(request)
    return redirect('home')