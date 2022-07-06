



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
        popup.classList.toggle("showPopUp");
        table.classList.toggle("blure"); 
    });

    const main = document.querySelector(".main"); 
    main.addEventListener("click", function (e) {
    const target = e.target; 

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
  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
});




/*forme pour envoyer un fichier */ 
function FormSubmit() {

  var formData = readData(); 
  console.log(formData);
  insertFille(formData);
  resetForm();

}

function readData() {
    var formData = {};
    formData["Name"] = document.getElementById("Name").value;
    formData["Recipient"] = document.getElementById("Recipient").value;
    formData["Description"] = document.getElementById("Description").value; 
    return formData;
}


/*
function insertFille(data) {
    var table = document.querySelector("table").getElementsByTagName('tbody')[0];
    var newRow = table.insertRow(table.length);
    cell1 = newRow.insertCell(0);
    cell1.innerHTML = `<div class="fileFirstInfo">
                            <h id="fileName">Titre</h>
                            <h id="fileDate">Date</h>
                        </div>
                        
                        <div class="fileOptions">
                            <div class="description">
                                <h id="descriptionBtn">Description2</h>
                            </div>
                            
                            <div class="optionsBtn">

                                <button class="fileBtn" id="previewBtn">Aperçu</button>
                                <button class="fileBtn" id="downloadBtn">Télécharger</button>
                                <button class="fileBtn" id="delFileBtn" onClick="Delete(this)">Supprimer</button>

                            </div>

                        </div>`;

                        // addonElement.innerHTML = "<div class="fileFirstInfo">" + data.className + "'>" +
                        // "Your favorite color is now " + data.color +
                        // "</div>";
}
*/

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

  