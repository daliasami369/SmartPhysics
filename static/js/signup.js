function openSignUpModal() {

    document.getElementById("signupmodel").style.display = "flex";

}

function closesignupModal() {

    document.getElementById("signupmodel").style.display = "none";

}

function openloginModal() {

    document.getElementById("loginmodel").style.display = "flex";

}

function closeloginModal() {

    document.getElementById("loginmodel").style.display = "none";

}

async function handleSubscribeClick() {
    let email = prompt("Please ,Enter Your Email !")
    if (!email)
        return;
    let response = await fetch('/check-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ email: email })
    })
    let data = await response.json();
    console.log(data);
    if (data.exists) {
        openloginModal();
    }
    else {
        openSignUpModal();
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function handleLogin(event) {

    event.preventDefault();

    const email = document.querySelector("#loginmodel input[name='email']").value;
    const password = document.querySelector("#loginmodel input[name='Password']").value;

    const response = await fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (data.success) {

        window.location.href = data.redirect;

    } else {

        alert(data.message);

    }
}

async function handleSignup(event) {

    event.preventDefault();

    const username = document.querySelector("#signupmodel input[name='UserName']").value;
    const password = document.querySelector("#signupmodel input[name='Password']").value;
    const email = document.querySelector("#signupmodel input[name='email']").value;
    const phone = document.querySelector("#signupmodel input[name='phone']").value;
    const parent_phone = document.querySelector("#signupmodel input[name='parent_phone']").value;
    const parent_email = document.querySelector("#signupmodel input[name='parent_email']").value;
    const address = document.querySelector("#signupmodel input[name='address']").value;

    const level = document.querySelector("#signupmodel input[name='level']:checked")?.value;

    const response = await fetch("/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email,
            parent_email: parent_email,
            phone: phone,
            parent_phone: parent_phone,
            address: address,
            level: level
        })
    });

    const data = await response.json();

    if (data.success) {

        showMessage("تم إنشاء الحساب بنجاح ✔", "success");

        setTimeout(() => {
            closesignupModal();
            openloginModal();
        }, 2000);

    } else {

        showMessage(data.message, "error");

    }

}
function showMessage(message, type) {

    const box = document.getElementById("signupMessage");

    box.innerText = message;

    box.className = type;

    box.style.display = "block";

    setTimeout(() => {
        box.style.display = "none";
    }, 3000);

}