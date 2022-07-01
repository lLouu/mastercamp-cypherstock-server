// const
const api_url = "localhost:3443"
const iteration = 100000


// html generation

const insert_button = async(name, href = null, disable=true, onclick=null) => {
    let ret = document.createElement("button");
    ret.textContent = name;
    ret.appendChild(document.createElement("span"));
    ret.appendChild(document.createElement("span"));
    ret.appendChild(document.createElement("span"));
    ret.appendChild(document.createElement("span"));
    if(href){ret.href = href;}
    if(onclick){ret.setAttribute('onclick', onclick);}
    if(disable){ret.setAttribute('class', "js-disabled");}
    document.getElementById("buttons").appendChild(ret);
    return ret;
}

const flush_buttons = async() => {
    let but = document.getElementById('buttons');
    but.innerHTML = '';
}

const insert_input = async(placeholder, name, type, listner = null) => {
    let ret = document.createElement("input");
    ret.setAttribute('type', type);
    ret.setAttribute('placeholder', placeholder);
    ret.setAttribute('name', name);
    ret.setAttribute('id', name);
    document.getElementById("inputs").appendChild(ret);
    if(listner != null){ret.addEventListener("keydown", listner, false);}
    return ret;
}

const insert_input_div = async(id) => {
    let ret = document.createElement("div");
    ret.setAttribute('class', "flex row");
    ret.setAttribute('id', id);
    if(id == "words"){
        ret.innerHTML = '<div id="12"><input type="radio" name="nbmots" value="12" checked><label for="12">12 MOTS</label></div><div id="24"><input type="radio" name="nbmots" value="24"><label for="24">24 MOTS</label></div>';
    }else{
        ret.innerHTML = '<input type="checkbox" name="Authentification de 2 facteurs" class="style3" id="f" value="Authendification 2 Facteurs"><label for="checkbox">Autentification 2 Facteurs </label>';
    }
    document.getElementById("inputs").appendChild(ret);
    return ret;
}

const flush_inputs = async() => {
    let inp = document.getElementById('inputs');
    inp.innerHTML = '';
}


// views setup

const set_login = async() => {
    flush_buttons();
    flush_inputs();

    insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
    insert_input("MOT DE PASSE", "password", "password");

    insert_button("Se Connecter", null, false, "login();");
    insert_button("S'inscrire", "/signup");
}

const set_sign_up = async() => {
    flush_buttons();
    flush_inputs();

    insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
    insert_input("PSEUDO", "pseudo", "text", alnum);
    insert_input("MOT DE PASSE", "password", "password");
    insert_input_div("words");
    insert_input_div("FA");

    insert_button("S'inscrire", null, false, "sign_up();");
    insert_button("Utiliser sa seed", null, false, "recover();");
    insert_button("Se connecter", "/login");
}

const recover = async() => {
    flush_buttons();
    flush_inputs();

    insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
    insert_input("SEED", "seed", "string", seed);
    
    insert_button("Retrouver", null, false, "seed_recovery();");
    insert_button("Retour", null, false, "set_sign_up();");
}


// input verifyer

const wrong_entry = async(ele) => {
    ele.style.border = "2px solid red";
    ele.style.outline = "none";
}

const alnum = (e) => {
    if(e.key.search(/^[a-z0-9]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
}

const num = (e) => {
    if(e.key.search(/^[0-9]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
}

const seed = (e) => {
    if(e.key.search(/^[a-z ]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
}


// backend

// better request
const send_request = async(url, content = null, name = null, desc = null) => {
    let h = {"Connexion":"keep-alive"};
    if (name != null && name.replace(/^[a-z1-9]/i, '' != '')){h["XEU-name"] =  name;}
    if (desc != null && name.replace(/^[a-z1-9 ,.]/i, '' != '')){h["XEU-desc"] = desc}
    if (content != null){h["Content-type"] = "text/plain";}
    return fetch(url, {
        method: "POST",
        headers: h,
        body: content
    });
}


// pkey AES
//ab2str & str2ab from https://stackoverflow.com/questions/6965107/converting-between-strings-and-arraybuffers
const ab2str = (buf) => {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}
  
const str2ab = (str) => {
    var buf = new ArrayBuffer(str.length*2); 
    var bufView = new Uint8Array(buf);
    for (var i=0, strLen=str.length; i<strLen; i++) {
      bufView[i] = str.charCodeAt(i);
    }
    return buf;
}


const deriv_key = async(pwd, s, iteration) => {
    return await window.crypto.subtle.deriveKey({
        name: "PBKDF2",
        hash: "SHA-256",
        salt: s,
        iterations: iteration
    }, 
    await window.crypto.subtle.importKey("raw", str2ab(pwd), "PBKDF2", false, ["deriveKey"]), 
    {
        name: "AES-CBC",
        length: 256
    }, 
    true, 
    ["encrypt", "decrypt"]);
}

const salt = (n = 16) => {
    let buffer = new Uint8Array(n);
    return window.crypto.getRandomValues(buffer);
}

const encrypt = async(pkey, pwd) => {
    let s = salt()
    let epkey = (await window.crypto.subtle.encrypt({
        name: "AES-CBC",
        iv: s
    }, await deriv_key(pwd, s, iteration), pkey), s, iteration);
    console.log(epkey);
    return epkey;
}

const decrypt = async(epkey, pwd) => {
    return await window.crypto.subtle.decrypt({
        name: "AES-CBC",
        iv: epkey[1]
    }, await deriv_key(pwd, epkey[1], epkey[2]), epkey[0]);
}


// token generation
const gen_token = (id, pkey) => {

}


// general backend
const login = async() => {
    let epkey = window.localStorage.getItem("epkey");
    if(!epkey){
        let FA = document.getElementById("FA");
        if(FA == null){
            let inputs = document.getElementById("inputs");
            for(let i = 0; i < inputs.childElementCount; i++){
                inputs.children[i].style.display = "none";
            }
            let instructions = document.createElement("p");
            instructions.textContent = "Vous n'avez pas vos données encryptées en local<br>Si vous avez activé l'Authentification 2 facteurs, retrouvez les données en indiquant votre token<br>Sinon, retrouver votre compte via votre seed par l'inscription.";
            inputs.appendChild(instructions);
            insert_input("A2F", "FA", "text", num);

            flush_buttons();
            insert_button("Valider", null, false, "login();");
            insert_button("Retour", null, false, "set_login();");
        }else{
            send_request("%s/?command=0&fa=%s&id=%s"%(api_url, FA.content, id)).then(res => {
                window.localStorage.setItem("epkey", res.text);
                login();
            });
        }
    }
    let id = document.getElementById("username").content;
    if(id.replace(/^[a-z0-9]/i, '') != ''){return;} // Manage this error
    let pwd = document.getElementById("password").content;
    let token = gen_token(id, decrypt(epkey, pwd));
    send_request("%s/?auth=%s&command=4&id=%s"%(api_url, token, id)).then(res => {
        window.sessionStorage.setItem("token", token);
        history.pushState(null, null, "/");
    });
}

const sign_up = async() => {
    
}

const seed_recovery = async() => {

}


// routing

const navTo = async(url) => {
    history.pushState(null, null, url);
    route();
}

const route = function (){
    path = window.location.pathname;
    if(path == "/login"){
        set_login();
    }
    else{
        if(path == "/signup"){
            set_sign_up();
        }
        else{
            window.location.href = "/login";
        }
    }
}

window.onload = () => {
    route();
    a = encrypt("test", "tuturu").then(e => {
        console.log(e);
        // b = decrypt(a, "tuturu").then(e => {console.log(e)});
    });
};


// Event listners

// Signgle page button
document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", e => {
        if("js-disabled" == e.target.classList[0]){
            e.preventDefault();
            navTo(e.target.href);
        }
    },false);
}, false);

// Single page history
window.addEventListener("popstate", route, false);

