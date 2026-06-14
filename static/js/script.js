

document.addEventListener("DOMContentLoaded",function(){
    const noteInput =document.getElementById("noteInput");
    const uploadBtn=document.getElementById("uploadBtn");

    uploadBtn.addEventListener("click",function(){
        alert("Uploading...");
        const noteContent=noteInput.value;
        fetch("/api/save-note",{
            method:'POST',headers:{'Content-Type':'application/json'},
            body: JSON.stringify({mynote:noteContent})
        }).then(response=>response.json())
        .then(data=>{console.log("Note saved: ", data);loadNotes()})
        .catch(error=>console.error('Error:', error));

    });

    loadNotes();

});

function loadNotes() {
    fetch("/api/list-notes")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("notesList");    //the empty list
            list.innerHTML = "";

            data.files.forEach(key => {   //build-in method to traverse array
                const li = document.createElement("li");  //create a <li> element

                li.innerHTML = `
                    ${key}<button class="margin inline_btn" onclick="downloadNote('${key}')">Download</button><button class="margin inline_btn" onclick="deleteNote('${key}')">Delete</button>
                `;

                list.appendChild(li);
            });
        })
        .catch(err => console.error("Error loading notes:", err));
}

function downloadNote(key){  //go to this url, if return file download it
    window.location.href=`/api/download-note?filekey=${encodeURIComponent(key)}`    //make file name safe for url syntax
}

function deleteNote(key){
    fetch(`/api/delete-note?filekey=${encodeURIComponent(key)}`,{method:"DELETE"})
    .then(res=>res.json())
    .then(data=>{
        console.log("Deleted:", data);
        loadNotes();
    })
    .catch(err=>console.error("Delete error",error))
}