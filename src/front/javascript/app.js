



document.addEventListener("DOMContentLoaded", () => {
    /*menu de côté*/ 
    const menuIcon = document.querySelector(".menuButton"); 
    const navbar = document.querySelector(".navbar");
    menuIcon.addEventListener("click", ()=> {
        navbar.classList.toggle("change");
    });

    /*menu de bas*/
    const settingsIcon = document.querySelector(".avatar"); 
    const settingsMenu = document.querySelector(".settingsMenu");
    settingsIcon.addEventListener("click", ()=> {
        settingsMenu.classList.toggle("show");
    });

    /*file uploade*/
    const upload = document.querySelector(".addFile");
    const popup = document.querySelector(".uploadPopUp");
    const table = document.querySelector("table");
    upload.addEventListener("click", ()=> {
      table.style.display ="none"; 
      popup.style.display ="flex"; 
    });

    const main = document.querySelector(".main"); 
    main.addEventListener("click", function (e) {

      const target = e.target;
      
      //fermeture de formulaire avec le click sur le main 
      if(target == main){
        popup.style.display ="none"; 
        table.style.display ="flex"; 
      }
  
      /*fermeture des parties actives */ 
       const activeFile = document.querySelector(".fileFirstInfo.showFile");
       const activeOpt = document.querySelector(".fileOptions.showOption");
  
      //if(currentlyActiveFile && target.matches(".fileFirstInfo")) {
  
      if(activeFile && activeFile != target) {
           activeFile.classList.toggle("showFile");
           activeOpt.classList.toggle("showOption");
      }
  
      /*ouverture*/ 
      if (target.matches(".fileFirstInfo")){
          target.classList.toggle("showFile");
          const fileOpt = target.nextElementSibling;
          fileOpt.classList.toggle("showOption");
      }
  
  });

  /*drag and drop */
  document.querySelectorAll(".file_input").forEach((inputElement) => {
    const dropZoneItem = inputElement.closest(".uploade-zone");

    dropZoneItem.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateFiel(dropZoneItem, inputElement.files[0]);
      }
    });

    dropZoneItem.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneItem.classList.add("uploade-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneItem.addEventListener(type, (e) => {
        dropZoneItem.classList.remove("uploade-zone--over");
      });
    });

    dropZoneItem.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateFiel(dropZoneItem, e.dataTransfer.files[0]);
      }

      dropZoneItem.classList.remove("uploade-zone--over");
    });

  });
});




/*forme pour envoyer un fichier */ 
// function FormSubmit() {

//   var formData = readData(); 
//   insertFille(formData);
//   resetForm();

// }

// function readData() {
//     var formData = {};
//     formData["Name"] = document.getElementById("Name").value;
//     formData["Recipient"] = document.getElementById("Recipient").value;
//     formData["Description"] = document.getElementById("Description").value; 
//     return formData;
// }

function resetForm() {
    document.getElementById("Name").value = "";
    document.getElementById("Recipient").value = "";
    document.getElementById("Description").value = "";
}

function Delete(td) {
    if (confirm('Voulez-vous supprimer ce fichier')) {
        row = td.parentElement.parentElement;
        document.querySelector("table").deleteRow(row.rowIndex);
    }
}

function updateThumbnail(dropZoneElement, file) {
  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").remove();
  }

  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;
}

const add_profile = (id) => {
  let ret = document.createElement("li");
  ret.appendChild(document.createElement("button"));
  ret.firstChild.setAttribute("class", "profilBtn");
  ret.firstChild.setAttribute("onclick", "get_infos('" + id + "');");
  let img = document.createElement("img");
  img.setAttribute("class", "profilImage");
  img.src = "rcs/profil_icon.png";
  ret.firstChild.appendChild(img);
  let a = document.createElement("a");
  a.textContent = id;
  ret.firstChild.appendChild(a);

  document.getElementById("profil").appendChild(ret);
  return ret;
}

const add_document = (title, date, desc) => {
  let ret = document.createElement("tr");
  ret.appendChild(document.createElement("td"));

  let fileFirstInfo = document.createElement("div");
  fileFirstInfo.setAttribute("class", "fileFirstInfo");
  let h1 = document.createElement("h");
  h1.textContent = title;
  let h2 = document.createElement("h");
  h2.textContent = date;
  fileFirstInfo.appendChild(h1);
  fileFirstInfo.appendChild(h2);

  let description = document.createElement("div");
  description.setAttribute("class", "description");
  description.appendChild(document.createElement("h"));
  description.firstChild.textContent = desc;

  let optionsBtn = document.createElement("div");
  optionsBtn.setAttribute("class", "optionsBtn");
  let app = document.createElement("button");
  app.setAttribute("class", "fileBtn");
  app.textContent = "Aperçu";
  let tel = document.createElement("button");
  tel.setAttribute("class", "fileBtn");
  tel.textContent = "Télécharger";
  let del = document.createElement("button");
  del.setAttribute("class", "fileBtn");
  del.textContent = "Supprimer";
  optionsBtn.appendChild(app);
  optionsBtn.appendChild(tel);
  optionsBtn.appendChild(del);

  let fileOptions = document.createElement("div");
  fileOptions.setAttribute("class", "fileOptions");
  fileOptions.appendChild(description);
  fileOptions.appendChild(optionsBtn);

  ret.appendChild(fileFirstInfo);
  ret.appendChild(fileOptions);

  document.getElementById("table").appendChild(ret);
  return ret;
}

const get_infos = (id) => {
  send_request(api_url + "/?auth=" + window.sessionStorage.getItem("token") + "&command=2&id="+id).then(res => {
    if(res.ok){
      res.text().then(res => {
        document.getElementById("table").innerHTML = '';
        let arr = res.split('\n\n');
        let i = 0;
        while(arr[i] != ''){
          let infos = arr[i].split('-');
          let date = new Date(parseInt(infos[1])*1000);
          let d = date.getDate().toString() + "/" + date.getMonth().toString() + "/" + date.getFullYear().toString();
          add_document(infos[0], d, infos[3]);
          i++;
        }
      });
    }
  });
}

const disconnect = () => {
  window.sessionStorage.removeItem('token');
  window.location.href = '/login';
}

const delete_account = () => {
  if(confirm("Êtes vous sur de vouloir supprimer définitivement votre compte ?")){
    send_request(api_url + "?/auth=" + token).then(res => {
      if(res.ok){
        res.text().then(res => {
          if(res == "success"){
            disconnect();
          }
        });
      }
    });
  }
}

const upload_func = async() => {
  let ab = document.getElementById("up").files[0].arrayBuffer();
  let dest = document.getElementById("Recipient").value.split(' ');
  dest.push(window.sessionStorage.getItem("id"));
  let title = document.getElementById("Name").value;
  let desc = document.getElementById("Description").value;

  
  let key = window.crypto.subtle.generateKey({
    name:"AES-CBC",
    length: 256
  }, true, ["encrypt", "decrypt"]);
  let sym = [];
  let i = 0;
  while(dest[i] != undefined){
    let res = await send_request(api_url + "/?auth=" + window.sessionStorage.getItem("token") + "&command=5&id=" + dest[i])
    if(res.ok){
      let pubkey = await window.crypto.subtle.importKey("spki", cpem2ab(await res.text()), {
        name: "RSA-OAEP",
        hash: "SHA-256"
        }, false, ["encrypt"])
      
      sym.push(ab2hex(await window.crypto.subtle.encrypt(
        {name: "RSA-OAEP"}, pubkey, await window.crypto.subtle.exportKey("raw", await key)
      )));
    }
    i++;
  }

  ab = await ab;
  let enc_file = await window.crypto.subtle.encrypt({
    name: "AES-CBC",
    iv: salt()
  }, await key, ab);

  send_request(api_url + "/?auth=" + window.sessionStorage.getItem("token") + "&command=8&id=" + dest.join('-') + "&sym=" + sym.join('-'), enc_file, title, desc).then(res => {
    if(res.ok){
      const popup = document.querySelector(".uploadPopUp");
      const table = document.querySelector("table");
      popup.style.display ="none"; 
      table.style.display ="flex";
      resetForm();
    }
  })
}


const set_dark = () => {
  document.getElementById("mode").href = "css/dark.css"
}

const set_light = () => {
  document.getElementById("mode").href = "css/light.css"
}

window.onload = () => {
  let token = window.sessionStorage.getItem("token");
  if(token == null){
    window.location.href = "/login";
  }

  send_request(api_url + "/?auth=" + token + "&command=1").then(res => {
    if(res.ok){
      res.text().then(res => {
        let arr = res.substr(1, res.length-2).split(', ');
        let i = 0;
        while(arr[i] != undefined){
          add_profile(arr[i].split("'")[1]);
          i++;
        }
      });
    }
  });
  let id = token.split('-')[0];
  document.getElementById("name").textContent = id;
  window.sessionStorage.setItem("id", id);
}
  