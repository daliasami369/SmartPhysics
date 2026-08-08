from django.db import models

# Create your models here.
class User(models.Model):

    ROLE_CHOICES = [
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    ]

    LEVEL_CHOICES = [
        ("First_Secondary", "First Secondary"),
        ("Second_Secondary", "Second Secondary"),
        ("Third_Secondary", "Third Secondary"),
    ]

    username = models.CharField(max_length=100)

    password = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=100)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Student"
    )

    level = models.CharField(
        max_length=100,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(default=False)

    payment_end = models.DateField(blank=True, null=True)

    parent_phone = models.CharField(  max_length=20, blank=True, null=True )

    parent_email = models.EmailField( blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

class Test(models.Model):

    teacher = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    duration = models.IntegerField()

    description = models.TextField(blank=True)

    level = models.CharField(max_length=100 , blank=True,null=True)
    total_marks = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    mark = models.IntegerField(default=1)

class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(max_length=200)

    is_correct = models.BooleanField(default=False)

class StudentResult(models.Model):

    student=models.ForeignKey(User,on_delete=models.CASCADE)

    test=models.ForeignKey(Test,on_delete=models.CASCADE)

    score=models.IntegerField()

    total_marks=models.IntegerField()

    submitted_at=models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):

    teacher = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    level = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=6, decimal_places=2)

    lesson_type = models.CharField(
    max_length=20,
    choices=[
        ("recorded", "Recorded"),
        ("live", "Live"),
    ],
    default="recorded"
)

    pdf_file = models.FileField(
    upload_to="lesson_pdfs/",
    blank=True,
    null=True
)

    video_link = models.TextField(blank=True,null=True)

    meeting_link = models.TextField(blank=True,null=True)

    live_date = models.DateField(blank=True,null=True)

    live_time = models.TimeField(blank=True,null=True)

class LessonPayment(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE)

    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)

    receipt = models.ImageField(
    upload_to="receipts/",
    blank=True,
    null=True
)

    status = models.CharField(
        max_length=20,
        default="Pending"
    )
class Announcement(models.Model):

    teacher=models.ForeignKey(User,on_delete=models.CASCADE)

    title=models.CharField(max_length=200)

    message=models.TextField()

    level=models.CharField(max_length=100)

    created_at=models.DateTimeField(auto_now_add=True)

class Message(models.Model):

    sender=models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE
    )

    receiver=models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE
    )

    message=models.TextField()

    created_at=models.DateTimeField(auto_now_add=True)
    
class Homework(models.Model):

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    level = models.CharField(max_length=100)

    file = models.FileField(
        upload_to="homeworks/"
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )