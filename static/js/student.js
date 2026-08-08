console.log("student page")

window.onload=function(){
   const studentname=document.getElementById("studentName");
   const name=localStorage.getItem('username')
   if(name){
        studentname.textContent =name;

   }

   if(localStorage.getItem("dark")=="true"){

document.body.classList.add("dark");

document.getElementById("darkMode").checked=true;

}

     openStudentChat();  
}

function showSection(sectionName){
    console.log(sectionName);
    const sections = [
        "chatSection",
        "lessonsSection",
        "testsSection",
        "profileSection",
        "settingsSection",
        "announcementsSection",
        "homeSection",
        "homeworkSection"
    ];

    sections.forEach(function(id){

        const section = document.getElementById(id);

        if(section){
            section.style.display = "none";
        }

    });
    if(sectionName=="home"){
    document.getElementById("homeSection").style.display="block";
    }
    else if(sectionName=="chat"){
        document.getElementById("chatSection").style.display="block";
    }

   else if(sectionName=="lessons"){
        document.getElementById("lessonsSection").style.display="block";
    }

    else if(sectionName=="tests"){
        document.getElementById("testsSection").style.display="block";
    }
    else if(sectionName=="homework"){
        document.getElementById("homeworkSection").style.display="block";
    }
    else if(sectionName=="profile"){
        document.getElementById("profileSection").style.display="block";
    }

   else if(sectionName=="settings"){
        document.getElementById("settingsSection").style.display="block";
    }

    else if(sectionName=="announcements"){
        document.getElementById("announcementsSection").style.display="block";
    }

}

function CheckedPay(){

}

let editing = false;

async function editdata(){
     alert("clicked");

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

async function payLesson(lessonId){

    if(!confirm("هل تريد شراء هذا الدرس؟")){
        return;
    }

    const response = await fetch("/pay-lesson/",{

        method:"POST",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body: JSON.stringify({
            lesson_id: lessonId
        })

    });

    const data = await response.json();

    alert(data.message);

    if(data.success){
        location.reload();
    }

}

async function sendMessage(){

    const message =
    document.getElementById("studentMessage").value;

    if(message==""){
        alert("اكتب رسالة");
        return;
    }

    const formData = new FormData();

    formData.append("message",message);

    const response = await fetch("/send-message/",{

        method:"POST",

        headers:{
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:formData

    });

    const data = await response.json();

    if(data.success){

        document.getElementById("studentMessage").value="";

        openStudentChat();

    }

}
async function openStudentChat(){

    const response = await fetch("/student-chat/");

    const data = await response.json();

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = "";

    document.getElementById("chatTeacher").innerText = data.teacher;

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
