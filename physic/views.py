from django.shortcuts import render ,redirect,get_object_or_404
from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User ,Test,Question,Choice,StudentResult,Lesson,Announcement,Message,Homework,LessonPayment
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def teacher(request):

    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "Teacher":
        return redirect("student")
    print("Teacher:", user.username)
    print("Email:", user.email)
    print("Phone:", user.phone)
    # print("Context:", context)
    students_count = User.objects.filter(role="Student").count()
    lessons_count = Lesson.objects.filter(teacher=user).count()
    tests_count = Test.objects.filter(teacher=user).count()
    payments = LessonPayment.objects.select_related( "student", "lesson").filter( lesson__teacher=user, status="Pending")
    payment_count = LessonPayment.objects.filter(  lesson__teacher=user,  status="Pending").count()
    students = User.objects.filter(role="Student")
    students_with_messages = User.objects.filter(  role="Student",  sent_messages__receiver=user).distinct()
    paid_students = LessonPayment.objects.filter( lesson__teacher=user, status="Approved").values("student").distinct().count()
    unpaid_students = LessonPayment.objects.filter( lesson__teacher=user, status="Rejected").values("student").distinct().count()
    context = {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,

        "students_count": students_count,
        "lessons_count": lessons_count,
        "tests_count": tests_count,
        "payment_count": payment_count,
        "payments": payments,
        "students":students,
        "students_with_messages": students_with_messages,
        "paid_students":paid_students,
        "unpaid_students":unpaid_students,
    }
    print("Teacher:", user.username)
    print("Payments Count:", payments.count())
    print(payments)
    print(students)
    print(students.count())
    return render(request, "pages/teacher.html", context)

def signup(request):

    if request.method == "GET":
        return render(request, "pages/signup.html")

    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        phone = data.get("phone")
        parent_email = data.get("parent_email")
        parent_phone = data.get("parent_phone")
        address = data.get("address")
        level = data.get("level")

        if phone == parent_phone:
            return JsonResponse({
                "success": False,
                "message": "رقم الطالب لا يمكن أن يكون نفس رقم ولي الأمر."
            })

        if email == parent_email:
            return JsonResponse({
                "success": False,
                "message": "بريد الطالب لا يمكن أن يكون نفس بريد ولي الأمر."
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "هذا البريد مستخدم بالفعل."
            })

        User.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            phone=phone,
            parent_email=parent_email,
            parent_phone=parent_phone,
            address=address,
            level=level,
            role="Student"
        )

        return JsonResponse({
            "success": True
        })
    
def login(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({
                "success": False,
                "message": "Email not found"
            })

        if not check_password(password, user.password):
            return JsonResponse({
                "success": False,
                "message": "Wrong password"
            })

        request.session["user_id"] = user.id

        if user.role == "Teacher":
            return JsonResponse({
                "success": True,
                "redirect": "/teacher/"
            })

        return JsonResponse({
            "success": True,
            "redirect": "/student/"
        })
    
def student(request):

    if "user_id" not in request.session:
        return redirect("login")

    try:
        student = User.objects.get(id=request.session["user_id"])
    except User.DoesNotExist:
        return redirect("login")

    # منع المدرس من دخول صفحة الطالب
    if student.role != "Student":
        return redirect("teacher")
    lessons = Lesson.objects.filter(level=student.level)
    payments = LessonPayment.objects.filter(
    student=student,
    lesson__in=lessons
    )

    paid_lessons = payments.values_list("lesson_id", flat=True)
    announcements = Announcement.objects.filter( level=student.level).order_by("-created_at")
    tests = Test.objects.filter( level=student.level).order_by("-created_at")
    homeworks=Homework.objects.filter(level=student.level).order_by("-created_at")
    context = {

    "students": student,

    "username": student.username,
    "email": student.email,
    "phone": student.phone,
    "level": student.level,

    "lessons": lessons,

    "paid_lessons": paid_lessons,

    "announcements": announcements,
    "tests": tests,
    "homeworks_count": homeworks.count(),
    "homeworks":homeworks,
    "lessons_count": lessons.count(),
    "tests_count": tests.count(),
    "learning_hours": lessons.count()*2,
    }
    print(student.level)
    print(Test.objects.values_list("level", flat=True))
    print("Student Level:", student.level)

    print("Announcements:")
    for a in announcements:
       print(a.title, a.level)

    print("Tests:")
    for t in tests:
       print(t.title, t.level)
    print("Student Level:", student.level)

    print("Announcements Count:", announcements.count())

    for a in announcements:
       print(a.title, a.level)

    return render(request, "pages/student.html", context)

def lesson_payment(request, lesson_id):
   
    if "user_id" not in request.session:
        return redirect("login")

    student = User.objects.get(id=request.session["user_id"])

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        print(request.FILES)
        print(request.FILES.get("receipt"))
        receipt = request.FILES.get("receipt")
        print("POST وصلت")

        print("Student:", student.username)

        print("Lesson:", lesson.title)

        print("Receipt:", receipt)
        payment, created = LessonPayment.objects.get_or_create(
              student=student,
              lesson=lesson,
              defaults={
                  "receipt": receipt,
                  "status": "Pending"
              }
              )
        print("Saved Successfully")
        if not created:
              payment.receipt = receipt
              payment.status = "Pending"
              payment.save()

        return JsonResponse({
            "success": True,
            "message": "تم إرسال طلب الدفع بنجاح."
        })

    return render(request, "pages/lesson_payment.html", {
        "lesson": lesson
    })


def check_user(request):
    if request.method =='POST':
        data =json.loads(request.body)
        email=data.get('email','').strip().lower()
        print("===================")
        print("email received:" ,email)
        exists=User.objects.filter(email__iexact=email).exists() 
        print("in email field:",  email)
        print("final: " ,exists)
        print("==============")

        return JsonResponse({'exists' :exists})

def update_profile(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user = User.objects.get(id=request.session["user_id"])

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()

        if not username or not email or not phone:
            return JsonResponse({
                "success": False,
                "message": "من فضلك املأ جميع البيانات."
            })

        user.username = username
        user.email = email
        user.phone = phone

        user.save()

        return JsonResponse({
            "success": True,
            "message": "تم حفظ البيانات"
        })

    return JsonResponse({
        "success": False
    })

def change_password(request):

    if request.method == "POST":

        data = json.loads(request.body)

        new_password = data.get("new_password")

        user = User.objects.get(id=request.session["user_id"])

        user.password = make_password(new_password)
        user.save()

        return JsonResponse({
            "success": True,
            "message": "تم تغيير كلمة المرور"
        })

    return JsonResponse({
        "success": False,
        "message": "طلب غير صحيح"
    })

def add_lesson(request):
    print("received")
    if request.method == "POST":

        teacher = User.objects.get(id=request.session["user_id"])

        Lesson.objects.create(
            teacher=teacher,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            video_link=request.POST.get("video_link"),
            level=request.POST.get("level"),
            price=request.POST.get("price"),
            pdf_file=request.FILES.get("pdf_file"),
            lesson_type="recorded"
        )

        return JsonResponse({
           "success": True,
            "message": "تم إضافة الدرس"
        })

    return JsonResponse({
        "success":False,
        "message":"Invalid Request"
    })

def watch_video(request, lesson_id):

    if "user_id" not in request.session:
        return redirect("login")

    student = User.objects.get(id=request.session["user_id"])

    lesson = get_object_or_404(Lesson, id=lesson_id)

    paid = LessonPayment.objects.filter(
    student=student,
    lesson=lesson,
    status="Approved"
    ).exists()

    if not paid:
        return HttpResponse("""
          <h2>🔒 هذا الدرس غير متاح حالياً.</h2>

          <p>يجب دفع ثمن الدرس أولاً أو انتظار مراجعة طلب الدفع.</p>

         <p>
         إذا كنت متأكدًا من أنك دفعت اشتراك هذه الحصة،
         يرجى التواصل مع فريق الدعم لمراجعة طلبك.
        </p>

          <p>
          📞 01098505909
            </p>

            <p>
           📧 smartphysics@instapay
           </p>
          """)

    return render(request, "pages/watch_video.html", {
        "lesson": lesson,
        "student": student
    })

def pay_lesson(request):

    if request.method == "POST":

        data = json.loads(request.body)

        lesson_id = data.get("lesson_id")

        student = User.objects.get(id=request.session["user_id"])

        lesson = Lesson.objects.get(id=lesson_id)

        LessonPayment.objects.get_or_create(
            student=student,
            lesson=lesson
        )

        return JsonResponse({
            "success": True,
            "message": "تم فتح الدرس بنجاح"
        })

    return JsonResponse({
        "success": False
    })

def approve_payment(request, payment_id):

    payment = get_object_or_404(
        LessonPayment,
        id=payment_id
    )

    payment.status = "Approved"

    payment.save()

    return redirect("teacher")

def reject_payment(request, payment_id):

    payment = get_object_or_404(
        LessonPayment,
        id=payment_id
    )

    payment.status = "Rejected"

    payment.save()

    return redirect("teacher")

def send_announcement(request):

    if request.method == "POST":

        teacher = User.objects.get(
            id=request.session["user_id"]
        )

        Announcement.objects.create(

            teacher=teacher,

            title=request.POST["title"],

            message=request.POST["message"],

            level=request.POST["level"]

        )

        return JsonResponse({
            "success":True,
            "message":"تم إرسال الإعلان."
        })

    return JsonResponse({"success":False})

def create_test(request):

    if request.method == "POST":

        teacher = User.objects.get(
            id=request.session["user_id"]
        )

        test = Test.objects.create(
             teacher=teacher,
           title=request.POST["title"],
           duration=request.POST["duration"],
            total_marks=request.POST["total_marks"],
            level=request.POST["level"]
       )

        return JsonResponse({
          "success": True,
          "test_id": test.id,
          "message": "تم إنشاء الاختبار"
        })

    return JsonResponse({
        "success": False
    })

def add_question(request):

    if request.method=="POST":

        test = Test.objects.get(
            id=request.POST["test_id"]
        )

        question = Question.objects.create(

            test=test,

            question=request.POST["question"],

            mark=request.POST["mark"]

        )

        Choice.objects.create(

            question=question,

            text=request.POST["choiceA"],

            is_correct=request.POST["correct"]=="A"

        )

        Choice.objects.create(

            question=question,

            text=request.POST["choiceB"],

            is_correct=request.POST["correct"]=="B"

        )

        Choice.objects.create(

            question=question,

            text=request.POST["choiceC"],

            is_correct=request.POST["correct"]=="C"

        )

        Choice.objects.create(

            question=question,

            text=request.POST["choiceD"],

            is_correct=request.POST["correct"]=="D"

        )

        return JsonResponse({

            "success":True,

            "message":"تم إضافة السؤال"

        })

    return JsonResponse({

        "success":False

    })

def add_homework(request):

    if request.method == "POST":

        if "user_id" not in request.session:
            return JsonResponse({
                "success": False,
                "message": "يجب تسجيل الدخول"
            })

        teacher = User.objects.get(
            id=request.session["user_id"]
        )

        Homework.objects.create(

            teacher=teacher,

            title=request.POST["title"],

            description=request.POST["description"],

            level=request.POST["level"],

            file=request.FILES.get("file"),

            deadline=request.POST["deadline"]

        )

        return JsonResponse({

            "success": True,

            "message": "تم إضافة الواجب بنجاح"

        })

    return JsonResponse({

        "success": False,

        "message": "طلب غير صالح"

    })

def send_message(request):

    if request.method == "POST":

        student = User.objects.get(id=request.session["user_id"])

        teacher = User.objects.filter(role="Teacher").first()

        Message.objects.create(
            sender=student,
            receiver=teacher,
            message=request.POST["message"]
        )

        return JsonResponse({
            "success": True,
            "message": "تم إرسال الرسالة"
        })

    return JsonResponse({
        "success": False
    })

def take_test(request, test_id):

    if "user_id" not in request.session:
        return redirect("login")

    student = User.objects.get(id=request.session["user_id"])

    test = get_object_or_404(Test, id=test_id)

    # منع إعادة الاختبار
    if StudentResult.objects.filter(
        student=student,
        test=test
    ).exists():

      result = StudentResult.objects.get(
        student=student,
        test=test
      )
   

      return render(request, "pages/test_result.html", {
              "score": result.score,
              "total_marks": test.total_marks,
              "finished": True
            })

    # عند الضغط على Submit
    if request.method == "POST":

        score = 0

        questions = test.questions.all()

        for question in questions:

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if answer:

                choice = Choice.objects.get(id=answer)

                if choice.is_correct:
                    score += question.mark

        StudentResult.objects.create(

              student=student,

              test=test,

               score=score,

               total_marks=test.total_marks

         )
        if student.parent_email:

            send_mail(
            subject="نتيجة الاختبار",
            message=f"""
              السلام عليكم

              ولي الأمر الكريم،

              قام الطالب: 
             {student.username}

                بحل اختبار:

                {test.title}

                وحصل على:

               {score} من {test.total_marks}

                  شكراً لكم.
                """,

                from_email=settings.EMAIL_HOST_USER,

                recipient_list=[student.parent_email],

                fail_silently=False
                 )

        return render(request, "pages/test_result.html", {

            "score": score,

            "total_marks": test.total_marks,

        })

    return render(request, "pages/take_test.html", {

        "test": test,

        "questions": test.questions.all()

    })

def test_results(request,test_id):

    test = get_object_or_404(Test,id=test_id)

    results = StudentResult.objects.filter(
        test=test
    ).select_related("student")

    return render(request,
                  "pages/show_test_results.html",
                  {
                      "test":test,
                      "results":results
                  })

def teacher_chat(request, student_id):

    teacher = User.objects.get(
        id=request.session["user_id"]
    )

    student = User.objects.get(
        id=student_id
    )

    messages = Message.objects.filter(

        sender__in=[teacher, student],

        receiver__in=[teacher, student]

    ).order_by("created_at")

    data = []

    for message in messages:

        data.append({

            "sender": message.sender.username,

            "message": message.message,

            "time": message.created_at.strftime("%H:%M")

        })

    return JsonResponse({

        "messages": data

    })

def send_teacher_message(request):

    if request.method == "POST":

        teacher = User.objects.get(
            id=request.session["user_id"]
        )

        student = User.objects.get(
            id=request.POST["student_id"]
        )

        Message.objects.create(

            sender=teacher,

            receiver=student,

            message=request.POST["message"]

        )

        return JsonResponse({

            "success": True,

            "message": "تم إرسال الرسالة"

        })

    return JsonResponse({

        "success": False

    })

def student_chat(request):

    student = User.objects.get(id=request.session["user_id"])

    teacher = User.objects.filter(role="Teacher").first()

    if not teacher:
        return JsonResponse({
            "teacher": "",
            "messages": []
        })

    messages = Message.objects.filter(
        sender__in=[student, teacher],
        receiver__in=[student, teacher]
    ).order_by("created_at")

    data = []

    for msg in messages:

        data.append({

            "sender": msg.sender.username,

            "message": msg.message,

            "time": msg.created_at.strftime("%H:%M")

        })

    return JsonResponse({

        "teacher": teacher.username,

        "messages": data

    })
