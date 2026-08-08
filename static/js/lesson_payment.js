document.getElementById("paymentForm").onsubmit = async function(e){
    console.log("lesson payment js loaded");
    e.preventDefault();

    const formData = new FormData();

    formData.append(
        "receipt",
        document.getElementById("receipt").files[0]
    );

    const response = await fetch(window.location.href,{
        method:"POST",
        headers:{
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    });

    const data = await response.json();

    alert(data.message);
    if(data.success){
        location.reload();
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