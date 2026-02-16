const chatbox = document.getElementById("chatbox");
// load saved theme
if(localStorage.getItem("theme")==="dark")
    document.body.classList.add("dark");


function addMessage(text,type){

    document.querySelector(".welcome")?.remove();

    let msg = document.createElement("div");
    msg.className = "bubble " + type;

    // format bot response
    if(type==="bot"){
        text = text
            .replace(/\n/g,"<br>")
            .replace("Description:","<br><b>🩺 Description</b><br>")
            .replace("Precautions:","<br><b>💊 Precautions</b><br>");
    }

    msg.innerHTML = text;

    chatbox.appendChild(msg);
    chatbox.scrollTop = chatbox.scrollHeight;
}


async function send(){
    let input = document.getElementById("msg");
    let text = input.value.trim();
    if(!text) return;

    addMessage(text,"user");
    input.value="";

    let typing = document.createElement("div");
    typing.className="bubble bot";
    typing.id="typing";
    typing.innerText="Typing...";
    chatbox.appendChild(typing);

    let res = await fetch("/predict",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:text})
    });

    let data = await res.json();
    document.getElementById("typing").remove();

    setTimeout(()=>addMessage(data.reply,"bot"),700);
}

document.getElementById("msg").addEventListener("keypress",e=>{
    if(e.key==="Enter") send();
});
document.getElementById("themeToggle").onclick = ()=>{
    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark"))
        localStorage.setItem("theme","dark");
    else
        localStorage.setItem("theme","light");
};

