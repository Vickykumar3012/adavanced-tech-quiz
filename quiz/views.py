from django.shortcuts import render,HttpResponse,redirect
from .models import Teacher,Student,Test,AttemptedTest,Question,Choice,OptedChoice
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
# Create your views here.

@login_required
def index(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
        return redirect('student_dashboard',id=student.id)
    except Student.DoesNotExist:
        teacher = Teacher.objects.get(user=user)
        return redirect('teacher_dashboard',id=teacher.id)
    # return render(request, "index.html")


def attempt_test(request,id):
    test = Test.objects.get(id=id)
    user = request.user
    student = Student.objects.get(user=user)
    try:
        x = AttemptedTest.objects.get(student=student,test=test)
    except AttemptedTest.DoesNotExist:
        x = AttemptedTest.objects.create(student=student,test=test)
    if x.is_submitted == True:
        return HttpResponse("Sorry you already attempted the test better luck next time")
    questions = test.question_set.all().order_by('id')
    choices = Choice.objects.filter(question__in=questions)
    paginator = Paginator(questions, 1)  # Show 1 question per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("The id of the question is",page_obj[0].id)
    try:
        selected_option = OptedChoice.objects.get(question=page_obj[0],attempted_test=x)
    except OptedChoice.DoesNotExist:
        selected_option = None

    context = {
        'questions':questions,
        'attempted_test':x,
        'choices':choices,
        'page_obj':page_obj,
        'selected_option':selected_option
    }
    return render(request, "quiz/attempt_test.html",context)


def save_response(request):
    if request.method == "POST":
        question_id = request.POST.get("attempted_question_id")
        choice_id = request.POST.get("choice")
        attempted_test_id = request.POST.get("attempted_test_id")
        print("The choice id is",choice_id)
        question = Question.objects.get(id=question_id)
        choice = Choice.objects.get(id=choice_id)
        attempted_test = AttemptedTest.objects.get(id=attempted_test_id)
        if choice.is_correct:
            attempted_test.score += question.marks
            attempted_test.save()
        hash = f"{question.id}+{attempted_test_id}"
        try:
            OptedChoice.objects.create(question=question,choice=choice,attempted_test=attempted_test,hash = hash)
        except:
            pass
            # OptedChoice.objects.create(question=question,choice=choice,attempted_test=attempted_test)
        # return to the same page from where it comes
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
def submit_test(request,test_id):
    
    test = AttemptedTest.objects.get(id=test_id)
    test.is_submitted=True
    test.save()
    print("I am in the function")
    return redirect('/')

    

def create_test(request):
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    Test.objects.create(name=name,description=desc)
    return redirect('teacher_dashboard',id=request.user.teacher.id)



def analyse(request,test_id):
    user = request.user
    student = Student.objects.get(user=user)
    test = Test.objects.get(id=test_id)
    try:
        attempted_test = AttemptedTest.objects.get(student=student,test=test)
    except:
        return HttpResponse("Please attempt the test first to see the analyses")
        
    question_count = test.all_question().count()
    attempt_count = OptedChoice.objects.filter(attempted_test=attempted_test).count()
    if(attempted_test.is_submitted):
        context = {
            "attempted_quiz":attempted_test,
            "count":question_count,
            "attempt_count":attempt_count
        }
        return render(request,"quiz/analyse.html",context)
    else:
        return HttpResponse("You have to attempt first to see the result")
    # attempted_test.is_submitted:
    #     context = {
    #         "attempted_quiz":attempted_test
    #     }
    #     return render("quiz/analyse.html",context)

    # attempted_test.is_submitted == True:
    #     pass
    # else:
    #     return HttpResponse("You have not submitted the tset yet")


def create_test_from_json(request):
    # Get the JSON data from the textarea
    json_data = request.POST.get('question')
    test_id = request.POST.get('test_id')
    print("The test id is",test_id)
    test = Test.objects.get(id=test_id)

    # Parse the JSON data into a Python object
    data = json.loads(json_data)

    # Create a new Test object
    # test = Test(name="Test from JSON", description="This test was created from JSON data")
    # test.save()

    # Loop through the questions in the JSON data and create a Question object for each one
    for question_data in data['questions']:
        # Create a new Question object for this question
        question = Question(test=test, text=question_data['question'], marks=1)
        question.save()

        # Loop through the options for this question and create a Choice object for each one
        for option in question_data['options']:
            # Check if this option is the correct answer (marked with an asterisk)
            is_correct = option.startswith('*')

            # Remove the asterisk from the option text
            text = option.lstrip('*')

            # Create a new Choice object for this option
            choice = Choice(question=question, text=text, is_correct=is_correct)
            choice.save()
    return redirect('teacher_dashboard',id=request.user.teacher.id)



def analyze_test_results(test):
    # Get all the questions in the test
    questions = Question.objects.filter(test=test)

    # Get all the choices that were selected for this test
    selected_choices = Choice.objects.filter(question__test=test)

    # Calculate the total number of questions
    total_questions = len(questions)

    # Calculate the number of questions that were attempted
    attempted_questions = len(set([choice.question_id for choice in selected_choices]))

    # Calculate the number of questions that were attempted correctly
    correct_choices = selected_choices.filter(is_correct=True)
    correct_questions = len(set([choice.question_id for choice in correct_choices]))

    # Calculate the number of questions that were attempted incorrectly
    incorrect_choices = selected_choices.filter(is_correct=False)
    incorrect_questions = len(set([choice.question_id for choice in incorrect_choices]))

    # Generate the analysis report
    report = f"Total questions: {total_questions}\n"
    report += f"Attempted questions: {attempted_questions}\n"
    report += f"Correctly attempted questions: {correct_questions}\n"
    report += f"Incorrectly attempted questions: {incorrect_questions}\n"

    return report
