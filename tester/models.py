from django.db import models
from django.conf import settings
from authenticator.models import Form, ClassArm


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(max_length=33)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='course/')
    is_active = models.BooleanField(default=False)
    form= models.ForeignKey(ClassArm, on_delete=models.CASCADE)
    mark = models.IntegerField(default=1)
    duration = models.IntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class TestSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.test.title} session"


class QuestionBank(models.Model):
    question_text = models.CharField(max_length=500)
    img = models.ImageField(upload_to='qimg/', null=True, blank=True)
    imginstr = models.CharField(max_length=200, null=True, blank=True)

    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)

    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_text} ({self.subject.name} - {self.form})"


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='qimg/', null=True, blank=True)
    imginstr = models.CharField( max_length=200, null=True, blank=True)
    question_text = models.CharField(max_length=500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.question_text} - {self.test}"


class TestResult(models.Model):
    user_key = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_arm_key = models.ForeignKey(ClassArm, on_delete=models.CASCADE)
    test_key = models.ForeignKey(Test, on_delete=models.CASCADE)

    username = models.CharField(max_length=100)
    svc_no = models.CharField(max_length=100)
    class_arm = models.CharField(max_length=100)
    test = models.CharField(max_length=100)
    score = models.IntegerField()

    desc = models.CharField(max_length=50)
    date = models.DateTimeField('date submitted')

    def __str__(self):
        return f"{ str(self.user_key) } { self.test } Test Result"
