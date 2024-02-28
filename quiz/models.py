from django.db import models
from django.contrib.auth.models import User
import json
from django.http import JsonResponse


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def all_question(self):
        return Question.objects.filter(test=self)
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    marks= models.IntegerField(default=1)

    def __str__(self):
        return self.text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class AttemptedTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name + " " + self.test.name
    
    def calculate_total_marks(self):
        questions = self.test.question_set.all()
        total_marks = 0
        for question in questions:
            total_marks += question.marks
        return total_marks
    
    def calculate_obtained_marks(self):
        total_marks =0
        opted_choices = OptedChoice.objects.filter(attempted_test = self)
        print("OPTED CHOICE COUNT",opted_choices.count())
        for x in opted_choices:
            if x.choice.is_correct==True:
                total_marks = x.choice.question.marks+total_marks
        print("Total marks i am getting is",total_marks)   
        return total_marks
    
    def calculate_store_percent(self):
        total_marks = self.calculate_total_marks()
        return (self.score/total_marks)*100
    
    # def calculate_correct_response(self):
        
    
class OptedChoice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    attempted_test = models.ForeignKey(AttemptedTest, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    hash  = models.CharField(max_length=100,blank=True,null=True,unique=True)

    def __str__(self):
        return self.attempted_test.student.name + " " + self.attempted_test.test.name + " " + self.choice.text
    

#  function that will accept a json from a body to create the question and choices
def create_test_by_json(request):
    if request.method == "POST":
        data = json.loads(request.body)
        test_name = data['test_name']
        test_description = data['test_description']
        questions = data['questions']
        test = Test.objects.create(name=test_name,description=test_description)
        for question in questions:
            question_text = question['question_text']
            question_marks = question['question_marks']
            choices = question['choices']
            question = Question.objects.create(test=test,text=question_text,marks=question_marks)
            for choice in choices:
                choice_text = choice['choice_text']
                choice_is_correct = choice['choice_is_correct']
                Choice.objects.create(question=question,text=choice_text,is_correct=choice_is_correct)
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"failed"})

    

