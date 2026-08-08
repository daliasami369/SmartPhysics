let currentTestId = null;
function showSection(sectionName){
    console.log(sectionName);
    sections=[
        "mystudentsSection",
        "homeSection",
        "announcementsSection",
        "lessonsSection",
        "chatSection",
        "testsSection",
        "statisticsSection",
        "profileSection",
        "settingsSection",
        "homeworkSection",
        "subscriptionsSection"
    ]

    sections.forEach( function(id){
         const section=document.getElementById(id)
         if(section)
         {
            section.style.display='none';
         }

    }
       
    );

     if(sectionName=='home')
    {
         document.getElementById('homeSection').style.display='block';
    }
    else  if(sectionName=='students')
    {
         document.getElementById('mystudentsSection').style.display='block';
    }
     else  if(sectionName=='subscriptions')
    {
         document.getElementById('subscriptionsSection').style.display='block';
         console.log(document.getElementById("subscriptionsSection"));
    }
    else if(sectionName=='homework')
    {
         document.getElementById('homeworkSection').style.display='block';
    }
     else if(sectionName=='lessons')
    {
         document.getElementById('lessonsSection').style.display='block';
    }
     else if(sectionName=='chat')
    {
         document.getElementById('chatSection').style.display='block';
    }
     else if(sectionName=='tests')
    {
         document.getElementById('testsSection').style.display='block';
    }
     else if(sectionName=='statistics')
    {
         document.getElementById('statisticsSection').style.display='block';
    }
    else if(sectionName=='announcements')
    {
         document.getElementById('announcementsSection').style.display='block';
    }
     else if(sectionName=='profile')
    {
         document.getElementById('profileSection').style.display='block';
    }
     else if(sectionName=='settings')
    {
         document.getElementById('settingsSection').style.display='block';
    }
}
let editing = false;

async function editdata(){
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const phone = document.getElementById("phone");

    const btn = document.getElementById("editBtn");

    if(!editing){

    username.disabled = false;
    email.disabled = false;
    phone.disabled = false;

    btn.innerText = "حفظ";

    editing = true;

    username.focus();

    return;
}else{
    

        const response = await fetch("/update-profile/",{

            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "X-CSRFToken":getCookie("csrftoken")
            },

            body:JSON.stringify({

                username:username.value,
                email:email.value,
                phone:phone.value

            })

        });

        const data = await response.json();

        if(data.success){

    username.disabled = true;
    email.disabled = true;
    phone.disabled = true;

    btn.innerText = "تعديل البيانات";

    editing = false;

    alert("تم حفظ البيانات");

}else{
    alert(data.message);
}

    }

}
function getCookie(name){

    let cookieValue = null;

    if(document.cookie && document.cookie !== ""){

        const cookies = document.cookie.split(";");

        for(let i = 0; i < cookies.length; i++){

            const cookie = cookies[i].trim();

            if(cookie.substring(0, name.length + 1) === (name + "=")){

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}

let editingPassword = false;

async function changePassword(){

    const pass = document.getElementById("pass");
    const confirmPass = document.getElementById("confirmPass");
    const btn = document.getElementById("passBtn");

    // أول ضغطة
    if(!editingPassword){

        pass.disabled = false;
        confirmPass.hidden = false;

        btn.innerText = "حفظ";

        pass.focus();

        editingPassword = true;

        return;
    }

    // التأكد من الإدخال
    if(pass.value == "" || confirmPass.value == ""){

        alert("اكتب كلمة المرور");

        return;
    }

    if(pass.value !== confirmPass.value){

        alert("كلمتا المرور غير متطابقتين");

        return;
    }

    // إرسال للسيرفر
    const response = await fetch("/change-password/",{

        method:"POST",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:JSON.stringify({

            new_password:pass.value

        })

    });

    const data = await response.json();

    alert(data.message);

    if(data.success){

        pass.value = "";
        confirmPass.value = "";

        pass.disabled = true;
        confirmPass.hidden = true;

        btn.innerText = "تغيير";

        editingPassword = false;
    }
}
const dark=document.getElementById("darkMode");

dark.addEventListener("change",function(){

document.body.classList.toggle("dark");

localStorage.setItem("dark",dark.checked);

});

async function addHomework(){

    const title =
    document.getElementById("homeworkTitle").value;

    const description =
    document.getElementById("homeworkDescription").value;

    const level =
    document.getElementById("homeworkLevel").value;

    const file =
    document.getElementById("homeworkFile").files[0];

    const deadline =
    document.getElementById("deadline").value;

    const formData = new FormData();

    formData.append("title",title);
    formData.append("description",description);
    formData.append("level",level);
    formData.append("file",file);
    formData.append("deadline",deadline);

    const response = await fetch("/add-homework/",{

        method:"POST",

        headers:{
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:formData

    });

    const data = await response.json();

    alert(data.message);
    if(data.success){

      document.getElementById("homeworkForm").reset();

}
}

async function addLesson(){
    alert("message")
    const formData = new FormData();

    formData.append("title", document.getElementById("lessonTitle").value);
    formData.append("description", document.getElementById("lessonDescription").value);
    formData.append("video_link", document.getElementById("lessonLink").value);
    formData.append("level", document.getElementById("lessonLevel").value);
    formData.append(  "price",  document.getElementById("lessonPrice").value );

    const pdf = document.getElementById("lessonPdf").files[0];

    if(pdf){
        formData.append("pdf_file", pdf);
    }

    const response = await fetch("/add-lesson/",{
        method:"POST",
        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },
        body:formData
    });

    const data = await response.json();

    if (data.success) {

    alert(data.message);

    document.getElementById("lessonTitle").value = "";
    document.getElementById("lessonDescription").value = "";
    document.getElementById("lessonLink").value = "";
    document.getElementById("lessonPdf").value = "";
    document.getElementById("lessonLevel").selectedIndex = 0;
    document.getElementById("lessonPrice").value = "";

}
else{
    alert(data.message);
}

}

document
.getElementById("announcementForm")
.onsubmit = async function(e){
    e.preventDefault();

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("title").value
    );

    formData.append(
        "message",
        document.getElementById("message").value
    );

    formData.append(
        "level",
        document.getElementById("AnnouncementLevel").value
    );

    const response = await fetch("/send-announcement/",{
        method:"POST",
        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },
        body:formData
    });
    const data = await response.json();

    alert(data.message);

    if(data.success){
        document.getElementById("announcementForm").reset();
    }

}

document.getElementById("testForm").onsubmit = createTest;
async function createTest(e){

    if(e){
        e.preventDefault();
    }

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("testTitle").value
    );

    formData.append(
        "duration",
        document.getElementById("duration").value
    );

    formData.append(
        "total_marks",
        document.getElementById("totalMarks").value
    );

    formData.append(
        "level",
        document.getElementById("testLevel").value
    );

    const response = await fetch("/create-test/",{

        method:"POST",

        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },

        body:formData

    });

    const data = await response.json();

    alert(data.message);

if(data.success){

    currentTestId = data.test_id;

    alert("تم إنشاء الاختبار، أضف الأسئلة الآن");

    document.getElementById("testForm").reset();

    document.getElementById("testsSection").style.display = "none";

    document.getElementById("questionsSection").style.display = "block";

}else{

    alert("حدث خطأ");

}

}

async function addQuestion(){

    const correct =
    document.querySelector("input[name='correct']:checked");

    if(!correct){
        alert("اختر الإجابة الصحيحة");
        return;
    }

    const formData = new FormData();

    formData.append("test_id", currentTestId);

    formData.append(
        "question",
        document.getElementById("questionText").value
    );

    formData.append(
        "choiceA",
        document.getElementById("choiceA").value
    );

    formData.append(
        "choiceB",
        document.getElementById("choiceB").value
    );

    formData.append(
        "choiceC",
        document.getElementById("choiceC").value
    );

    formData.append(
        "choiceD",
        document.getElementById("choiceD").value
    );

    formData.append(
        "mark",
        document.getElementById("mark").value
    );

    formData.append(
        "correct",
        correct.value
    );

    const response = await fetch("/add-question/",{

        method:"POST",

        headers:{
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:formData

    });

    const data = await response.json();

    alert(data.message);

    if(data.success){

        document.getElementById("questionText").value="";

        document.getElementById("choiceA").value="";

        document.getElementById("choiceB").value="";

        document.getElementById("choiceC").value="";

        document.getElementById("choiceD").value="";

        document.getElementById("mark").value="";

        document
        .querySelectorAll("input[name='correct']")
        .forEach(r=>r.checked=false);

    }

}
async function finishTest(){

    alert("تم حفظ الاختبار بنجاح");

    currentTestId=null;

    document.getElementById("questionsSection").style.display="none";

    document.getElementById("testsSection").style.display="block";

}
async function openTeacherChat(studentId, studentName){

    document.getElementById("studentId").value = studentId;

    document.getElementById("chatStudent").innerText = studentName;

    const response = await fetch(`/teacher-chat/${studentId}/`);

    const data = await response.json();

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = "";

    data.messages.forEach(msg=>{

        chatBox.innerHTML += `
            <div>
                <b>${msg.sender}</b> :
                ${msg.message}
                <small>${msg.time}</small>
            </div>
        `;

    });

}
async function sendTeacherMessage(){

    const studentId =
    document.getElementById("studentId").value;

    const message =
    document.getElementById("teacherMessage").value;

    if(message==""){

        alert("اكتب رسالة");

        return;

    }

    const formData = new FormData();

    formData.append("student_id",studentId);

    formData.append("message",message);

    const response = await fetch("/send-teacher-message/",{

        method:"POST",

        headers:{

            "X-CSRFToken":getCookie("csrftoken")

        },

        body:formData

    });

    const data = await response.json();

    if(data.success){

        document.getElementById("teacherMessage").value="";

        openTeacherChat(studentId,
        document.getElementById("chatStudent").innerText);

    }

}
