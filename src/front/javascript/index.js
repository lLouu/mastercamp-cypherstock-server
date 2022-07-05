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
};

const flush_buttons = async() => {
    let but = document.getElementById('buttons');
    but.innerHTML = '';
};

const insert_input = async(placeholder, name, type, listner = null) => {
    let ret = document.createElement("input");
    ret.setAttribute('type', type);
    ret.setAttribute('placeholder', placeholder);
    ret.setAttribute('name', name);
    ret.setAttribute('id', name);
    document.getElementById("inputs").appendChild(ret);
    if(listner != null){ret.addEventListener("keydown", listner, false);}
    return ret;
};

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
};

const flush_inputs = async() => {
    let inp = document.getElementById('inputs');
    inp.innerHTML = '';
};


// views setup

const set_login = async() => {
    flush_buttons().then(() => {
        insert_button("Se Connecter", null, false, "login();");
        insert_button("S'inscrire", "/signup");
    });

    flush_inputs().then(() => {
        insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
        insert_input("MOT DE PASSE", "password", "password");
    });
};

const set_sign_up = async() => {
    flush_buttons().then(() => {
        insert_button("S'inscrire", null, false, "sign_up();");
        // insert_button("Utiliser sa seed", null, false, "recover();"); // Seed option is unavailable since it need more work to be browserified
        insert_button("Se connecter", "/login");
    });


    flush_inputs().then(() => {
        insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
        insert_input("PSEUDO", "pseudo", "text", alnum);
        insert_input("MOT DE PASSE", "password", "password");
        insert_input_div("words");
        insert_input_div("FA");
    });
};

// seed recovery need more work to be browserified since window.crypto doesn't allow deterministic rsa keypair generation

// const recover = async() => {
//     flush_buttons().then(() => {
//         insert_input("NOM D'UTILISATEUR", "username", "text", alnum);
//         insert_input("SEED", "seed", "string", seed);
//     });

//     flush_inputs().then(() => {
//         insert_button("Retrouver", null, false, "seed_recovery();");
//         insert_button("Retour", null, false, "set_sign_up();");
//     });
// };



// rsa key gen

const gen_profile = async(pwd, secure = false, seed = null) => {
    // seed for client side on js is not simple since deterministic rsa key is not possible with window.crypto and bip39 is not browserified

    // if(seed == null){
    //     let master = await window.crypto.subtle.generateKey({
    //         name: "RSASSA-PKCS1-v1_5",
    //         modulusLength: 2048,
    //         publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
    //         hash: "SHA-256"
    //     }, false, ["deriv_key"])
    //     let raw_seed = await window.crypto.subtle.exportKey("raw",
    //     await window.crypto.subtle.deriveKey({
    //         name: "PBKDF2",
    //         hash: "SHA-256",
    //         salt : salt(),
    //         iterations: iteration
    //     }, master, {
    //         name: "HMAC",
    //         hash: "SHA-256",
    //         length: secure ? 32 : 16
    //     }, true, []));
    //     seed = gen_mnemotecnic(raw_seed);
    // }else{
    //     let raw_seed = recover_seed(seed);
    // }
    let key = await window.crypto.subtle.generateKey({
        name: "RSASSA-PKCS1-v1_5",
        modulusLength: 2048,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
        hash: "SHA-256"
    },
    true,
    ["sign", "verify"]);
    let pub = ab2cpem(await window.crypto.subtle.exportKey("spki", key.publicKey));
    let priv = await encrypt(ab2cpem(await window.crypto.subtle.exportKey("pkcs8", key.privateKey)), pwd);
    
    return {public: pub, private: priv};
};

const sign_up = async() => {
    let username = document.getElementById("username").value;
    let pseudo = document.getElementById("pseudo").value;
    let pwd = await window.crypto.subtle.digest("SHA-256", str2ab(document.getElementById("password").value));
    let secure = document.getElementById("24").firstChild.checked;
    let FA = document.getElementById("f").checked;

    let profile = await gen_profile(pwd, secure);
    let token = await gen_token(username, profile.private, pwd);

    window.localStorage.setItem(username + "epkey", profile.private);
    send_request(api_url + "/?auth=" + token + "&command=6&public=" + profile.public + "&pseudo=" + pseudo).then(res => {
        if(res.ok){
            res.text().then(res => {
                if(res == "success"){
                    window.sessionStorage.setItem("token", token);
                    if(FA){
                        // later
                    }
                    window.location.href = "/";
                }
            });
        }
    })
};

// general backend
const login = async() => {
    let id = document.getElementById("username").value;
    let epkey = window.localStorage.getItem(id + "epkey");
    if(!epkey){
        let FA = document.getElementById("FA");
        if(FA == null){
            let inputs = document.getElementById("inputs");
            for(let i = 0; i < inputs.childElementCount; i++){
                inputs.children[i].style.display = "none";
            }
            let instructions = document.createElement("p");
            instructions.innerHTML = "Vous n'avez pas vos donnees encryptees en local<br>Si vous avez active l'Authentification 2 facteurs, retrouvez les donnees en indiquant votre token<br>Sinon, retrouver votre compte via votre seed par l'inscription.";
            inputs.appendChild(instructions);
            insert_input("A2F", "FA", "text", num);

            await flush_buttons();
            insert_button("Valider", null, false, "login();");
            insert_button("Retour", null, false, "set_login();");
        }else{
            send_request(api_url + "/?command=0&fa=" + FA.value + "&id=" + id).then(res => {
                if(res.ok){
                    res.text().then(res => {
                        window.localStorage.setItem(id + "epkey", res);
                        login();
                    });
                }
            });
        }
    }
    // if(id.replace(/^[a-z0-9]/i, '') != ''){return;} // Manage this error
    let pwd = await window.crypto.subtle.digest("SHA-256", str2ab(document.getElementById("password").value));

    gen_token(id, epkey, pwd).then(token => {
        send_request(api_url + "/?auth=" + token + "&command=4&id=" + id).then(res => {
            if(res.ok){
                res.text().then(res => {
                    window.sessionStorage.setItem("pseudo", res);
                    window.sessionStorage.setItem("token", token);
                    window.location.href = "/";
                });
            }
        });
    }).catch(() => {
        console.log("wrong password");
        // wrong password
    });
};

// const seed_recovery = async() => {

// }


// routing

const navTo = async(url) => {
    history.pushState(null, null, url);
    route();
};

const route = function (){
    // let token = window.sessionStorage.getItem("token");
    // if(token != null && parseInt(token.split('-')[1])*1000 > Date.now()){
    //     window.location.href = "/";
    // }
    let path = window.location.pathname;
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
};

window.onload = route;


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
