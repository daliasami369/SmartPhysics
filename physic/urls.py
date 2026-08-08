from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('teacher/', views.teacher, name='teacher'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path('student/',views.student ,name='student'),
    path('check-user/',views.check_user , name='check_user'),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("add-lesson/", views.add_lesson, name="add_lesson"),
    path("pay-lesson/", views.pay_lesson, name="pay_lesson"),
    path("watch-video/<int:lesson_id>/", views.watch_video, name="watch_video"),
    path("lesson_payment/<int:lesson_id>/" ,views.lesson_payment,name='lesson_payment'),
    path( "approve-payment/<int:payment_id>/", views.approve_payment, name="approve_payment"),
    path( "reject-payment/<int:payment_id>/", views.reject_payment, name="reject_payment"),
    path( "send-announcement/", views.send_announcement, name="send_announcement"),
    path("create-test/", views.create_test, name="create_test"),
    path("add-question/", views.add_question, name="add_question"),
    path("add-homework/",views.add_homework,name="add_homework"),
    path(  "send-message/",  views.send_message,  name="send_message"),
    path( "take-test/<int:test_id>/", views.take_test, name="take_test"),
    path( "test-result/<int:test_id>/", views.test_results, name="test_results"),
    path( "teacher-chat/<int:student_id>/",  views.teacher_chat,  name="teacher_chat"),
    path("send-teacher-message/", views.send_teacher_message, name="send_teacher_message"),
    path("student-chat/", views.student_chat, name="student_chat"),
    path("send-message/", views.send_message, name="send_message"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )