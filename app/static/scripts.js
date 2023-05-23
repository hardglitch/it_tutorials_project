function setDropdown(elem_id) {
    document.getElementById(elem_id).classList.add("active");
    onClickOutside(elem_id)
}

function onClickOutside(elem_id) {
  document.addEventListener("click", event => {
    if (!document.getElementById(elem_id).contains(event.target))
        document.getElementById(elem_id).classList.remove("active");
  });
}

function addNewTType() {
    document.getElementById("t-type-value").innerText = document.getElementById("t-type-new").innerText.trim();
    document.getElementById("tutor-types-dropdown").classList.remove("active");
    document.getElementById("delete-type-button").style.display = "none"

    let type_values = document.querySelectorAll('[id^="type-value-"]');
    for (i=0; i<type_values.length; i++) {
        type_values[i].value = ""
    }

    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');
    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("submit-type-button-" + lang_code).value =
            document.getElementById("add-new-button-value").innerText.trim()
        document.getElementById("type-editor-form-" + lang_code).action =
            document.getElementById("type-editor-form-default-value").value
        document.getElementById("t-lang-code-" + lang_code).value = lang_code
        document.getElementById("t-type-code-" + lang_code).value = "";
        document.getElementById("type-editor-form-deleter").action = ""
    }
}

function changeTTypeAdmin(elem_id, ui_lang_code) {
    let type_code = elem_id.split("-").pop();
    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');

    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("type-value-" + lang_code).value = ""
        document.getElementById("type-value-" + lang_code).value =
            document.getElementById("type-value-" + lang_code + "-" + type_code).innerText.trim();

        document.getElementById("submit-type-button-" + lang_code).value =
            document.getElementById("save-button-value").innerText.trim()
        document.getElementById("type-editor-form-" + lang_code).action =
            "/" + ui_lang_code + "/type/" + type_code + "/edit"
        document.getElementById("t-lang-code-" + lang_code).value = lang_code

        document.getElementById("t-type-code-" + lang_code).value = "";
        document.getElementById("t-type-code-" + lang_code).value = type_code;

        document.getElementById("t-type-value").innerText
            = document.getElementById("type-value-" + ui_lang_code + "-" + type_code).innerText.trim();
        document.getElementById("tutor-types-dropdown").classList.remove("active");
        document.getElementById("delete-type-button").style.display = "block"
        document.getElementById("type-editor-form-deleter").action =
            "/" + ui_lang_code + "/type/" + type_code + "/del"
    }
}

function changeTType(elem_id) {
    document.getElementById("t-type-value").innerText = document.getElementById(elem_id).innerText.trim();
    let type_code = elem_id.split("-")[2]
    document.getElementById("t-type-code").value = type_code
    document.getElementById("tutor-types-dropdown").classList.remove("active");
    getAllowedThemes(type_code)
}

function getAllowedThemes(type_code = undefined) {
    if (type_code === undefined) {
        try {
            type_code = document.getElementById("t-type-code").value.trim()
        }
        catch (TypeError) {}
    }
    let divs = document.querySelectorAll('[id^="inherit-from-type-code-"]');
    for (i=0; i<divs.length; i++) {
        divs[i].style.display = "none"
    }
    let first = false;
    for (i=0; i<divs.length; i++) {
        if (divs[i].id.startsWith("inherit-from-type-code-"+type_code)) {
            if (first === false) {
                changeTTheme(divs[i].id)
                first = true
            }
            divs[i].style.display = ""
        }
    }
}

function changeTTheme(elem_id) {
    document.getElementById("t-theme-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("t-theme-code").value = elem_id.split("-").pop();
    document.getElementById("tutor-themes-dropdown").classList.remove("active");
}

function changeTLang(elem_id) {
    document.getElementById("t-lang-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("t-lang-code").value = elem_id.replace("t-lang-", "");
    document.getElementById("tutor-langs-dropdown").classList.remove("active");
}

function changeTDistType(elem_id) {
    document.getElementById("t-dist-type-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("t-dist-type-code").value = elem_id.replace("t-dist-type-", "");
    document.getElementById("tutor-dist-types-dropdown").classList.remove("active");
}
