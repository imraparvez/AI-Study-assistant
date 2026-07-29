async function sendQuestion() {
    document.getElementById("imageFile").addEventListener("change", function() {

    let file = this.files[0];

    if(file){

        let reader = new FileReader();

        reader.onload = function(e){

            let preview =
            document.getElementById("preview");

            preview.src = e.target.result;
            preview.style.display = "block";
        };

        reader.readAsDataURL(file);
    }

});

    let question =
    document.getElementById("question").value;

    let chatBox =
    document.getElementById("chat-box");

    let formData = new FormData();

    formData.append(
        "question",
        question
    );

    let pdf =
    document.getElementById("pdfFile").files[0];

    let image =
    document.getElementById("imageFile").files[0];

    if(pdf){
        formData.append("pdf", pdf);
    }

    if(image){
        formData.append("image", image);
    }

    chatBox.innerHTML += `
    <div class="user-msg">
    <b>You:</b> ${question}
    </div>
    `;

    document.getElementById("question").value = "";

    chatBox.innerHTML += `
    <div class="bot-msg" id="loading">
    <b>Bot:</b> Thinking...
    </div>
    `;

    try {

        let response = await fetch("/chat",{
            method:"POST",
            body:formData
        });

        let data = await response.json();

        document.getElementById(
            "loading"
        ).remove();

        chatBox.innerHTML += `
        <div class="bot-msg">
        <b>Bot:</b><br>
        ${data.answer.replace(/\n/g,"<br>")}
        </div>
        `;

    }
    catch(error){

        chatBox.innerHTML += `
        <div class="bot-msg">
        Error getting response
        </div>
        `;
    }

    chatBox.scrollTop =
    chatBox.scrollHeight;
}