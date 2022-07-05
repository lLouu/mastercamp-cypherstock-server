// const
const api_url = "http://localhost:3443";
const iteration = 100000;


// input verifyer

const wrong_entry = async(ele) => {
    ele.style.border = "2px solid red";
    ele.style.outline = "none";
};

const alnum = (e) => {
    if(e.key.search(/^[a-z0-9]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
};

const num = (e) => {
    if(e.key.search(/^[0-9]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
};

const seed = (e) => {
    if(e.key.search(/^[a-z ]/i) == -1){
        e.preventDefault();
        wrong_entry(e.target);
    }else{
        e.target.style = '';
    }
};


// backend

// better request
const send_request = async(url, content = null, name = null, desc = null) => {
    let h = {"Connexion":"keep-alive"};
    if (name != null && name.replace(/^[a-z1-9]/i, '') != ''){h["XEU-name"] =  name;}
    if (desc != null && name.replace(/^[a-z1-9 ,.]/i, '') != ''){h["XEU-desc"] = desc}
    if (content != null){h["Content-type"] = "text/plain";}
    return fetch(url, {
        method: "POST",
        headers: h,
        body: content
    });
};


// pkey AES
// ab2str & str2ab from https://stackoverflow.com/questions/6965107/converting-between-strings-and-arraybuffers
const ab2str = (buf) => {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
};
  
const str2ab = (str) => {
    var buf = new ArrayBuffer(str.length); 
    var bufView = new Uint8Array(buf);
    for (var i=0, strLen=str.length; i<strLen; i++) {
      bufView[i] = str.charCodeAt(i);
    }
    return buf;
};

// from https://stackoverflow.com/questions/42724367/js-convert-number-into-buffer-array4
const int2ab = num => [
    (num >> 24) & 255,
    (num >> 16) & 255,
    (num >> 8) & 255,
    num & 255,
  ];

const ab2int = ba => ((ba[0]*256+ba[1])*256+ba[2])*256+ba[3];

const hex2ab = h => {
    let ret = new Uint8Array(h.length/2);
    for(let i = 0; i < h.length/2; i++){
        ret[i] = parseInt(h[i*2] + h[i*2+1], 16);
    }
    return ret;
};

const ab2hex = ba => {
    return [...new Uint8Array(ba)]
        .map(x => x.toString(16).padStart(2, '0'))
        .join('');
};

// from https://stackoverflow.com/questions/40314257/export-webcrypto-key-to-pem-format
const ab2cpem = (keydata) => {
    let body = window.btoa(String.fromCharCode(...new Uint8Array(keydata)));
    return body.match(/.{1,64}/g).join('-');
};

const cpem2ab = (pem) => {
    return str2ab(window.atob(pem.replaceAll('-', '')));
};

const deriv_key = async(pwd, s, iteration) => {
    return await window.crypto.subtle.deriveKey({
        name: "PBKDF2",
        hash: "SHA-256",
        salt: s,
        iterations: iteration
    }, 
    await window.crypto.subtle.importKey("raw", pwd, "PBKDF2", false, ["deriveKey"]), 
    {
        name: "AES-CBC",
        length: 256
    }, 
    false, 
    ["encrypt", "decrypt"]);
};

const salt = (n = 16) => {
    let buffer = new Uint8Array(n);
    return window.crypto.getRandomValues(buffer);
};

const encrypt = async(pkey, pwd) => {
    let s = salt()
    let epkey = await window.crypto.subtle.encrypt({
        name: "AES-CBC",
        iv: s
    }, await deriv_key(pwd, s, iteration), str2ab(pkey));
    return ab2hex(s) + ab2hex(int2ab(iteration)) + ab2hex(new Uint8Array(epkey));
};

const decrypt = async(token, pwd) => {
    let s = hex2ab(token.slice(0, 32));
    let i = ab2int(hex2ab(token.slice(32, 40)));
    let epkey = hex2ab(token.slice(40));

    return ab2str(await window.crypto.subtle.decrypt({
        name: "AES-CBC",
        iv: s
    }, await deriv_key(pwd, s, i), epkey));
};

//signature
const sign = async(s, pkey) => {
    return ab2hex(await window.crypto.subtle.sign(
        "RSASSA-PKCS1-v1_5", 
        await window.crypto.subtle.importKey("pkcs8", pkey, {
            name: "RSASSA-PKCS1-v1_5",
            hash: "SHA-256"
            }, 
            false, 
            ["sign"]), 
        str2ab(s)));
};

// token generation
const gen_token = async(id, pkey, pwd) => {
    let timeout = window.localStorage.getItem(id + "timeout");
    if(timeout == null){
        timeout = "3600";
        window.localStorage.setItem(id + "timeout", timeout);
    }
    timeout = parseInt(timeout);
    timeout = (Math.floor(Date.now()/1000) + timeout).toString();
    return id + "-" + timeout + "-" + await sign(timeout, cpem2ab(await decrypt(pkey, pwd)));
};



