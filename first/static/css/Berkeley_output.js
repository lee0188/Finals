function menu(){
    var x = document.getElementById("berkelyBS");
    var y = document.getElementById("TC_lib");
    var z = document.getElementById("NT_lib");
    var btn1 = document.getElementById("btn1")
    var btn2 = document.getElementById("btn2")
    var btn3 = document.getElementById("btn3")
    if(x.style.display === 'none'){
        x.style.display = "block";
        y.style.display = 'none';
        z.style.display = 'none'
    }
    else{
        y.style.display = 'none';
        z.style.display = 'none'
    }

    btn1.classList.add('click')
    btn2.classList.remove('click')
    btn3.classList.remove('click')
}

function menu2(){
    var x = document.getElementById("berkelyBS");
    var y = document.getElementById("TC_lib");
    var z = document.getElementById("NT_lib");
    var btn1 = document.getElementById("btn1")
    var btn2 = document.getElementById("btn2")
    var btn3 = document.getElementById("btn3")

    y.classList.toggle("hide");
    if(y.style.display === 'none'){
        y.style.display = "block";
        x.style.display = 'none';
        z.style.display = 'none'
    }
    else{
        x.style.display = 'none';
        z.style.display = 'none'
    }

    btn1.classList.remove('click')
    btn2.classList.add('click')
    btn3.classList.remove('click')

}

function menu3(){
    var x = document.getElementById("berkelyBS");
    var y = document.getElementById("TC_lib");
    var z = document.getElementById("NT_lib"); 
    var btn1 = document.getElementById("btn1")
    var btn2 = document.getElementById("btn2")
    var btn3 = document.getElementById("btn3")

    z.classList.toggle("hide");  
    if(z.style.display === 'none'){
        z.style.display = "block";
        x.style.display = 'none';
        y.style.display = 'none';
    }
    else{
        x.style.display = 'none';
        y.style.display = 'none'
    }

    btn1.classList.remove('click')
    btn2.classList.remove('click')
    btn3.classList.add('click')
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
