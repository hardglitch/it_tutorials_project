function Test() {
    let fdata = new FormData(document.forms.namedItem("type-editor-form-26"))
    alert(document.getElementById("type-editor-form-26").action)
    // alert(fdata.get("word_code"))
    // alert(fdata.get("type_code"))
    // alert(fdata.get("lang_code"))
    // alert(fdata.get("type_value"))
}

function addNewTType() {
    document.getElementById("t-type-value").innerText = document.getElementById("t-type-new").innerText.trim();
    document.getElementById("tutor-types-dropdown").classList.remove("active");
    document.getElementById("delete-type-button").style.display = "none";

    let type_values = document.querySelectorAll('[id^="type-value-"]');
    for (i=0; i<type_values.length; i++) {
        type_values[i].value = "";
    }

    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');
    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("submit-type-button-" + lang_code).value =
            document.getElementById("add-new-button-value").innerText.trim();
        document.getElementById("type-editor-form-" + lang_code).action =
            document.getElementById("type-editor-form-default-value").value;
        document.getElementById("t-lang-code-" + lang_code).value = lang_code;
        document.getElementById("t-type-code-" + lang_code).value = "";
        document.getElementById("t-type-word-code-" + lang_code).value = "";
        document.getElementById("type-editor-form-deleter").action = "";
    }
}

function changeTTypeAdmin(elem_id, ui_lang_code) {
    let type_code = elem_id.split("-").pop();
    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');

    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();

        document.getElementById("type-value-" + lang_code).value = "";
        try {
            document.getElementById("type-value-" + lang_code).value =
                document.getElementById("type-value-" + lang_code + "-" + type_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("t-type-word-code-" + lang_code).value = "";
        try {
            document.getElementById("t-type-word-code-" + lang_code).value =
                document.getElementById("type-word-code-" + lang_code + "-" + type_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("submit-type-button-" + lang_code).value =
            (document.getElementById("type-value-" + lang_code).value !== "")
                ? document.getElementById("save-button-value").innerText.trim()
                : document.getElementById("add-new-button-value").innerText.trim()

        document.getElementById("type-editor-form-" + lang_code).action =
            "/" + ui_lang_code + "/type/" + type_code + "/edit";

        document.getElementById("t-lang-code-" + lang_code).value = lang_code;

        document.getElementById("t-type-code-" + lang_code).value = "";
        document.getElementById("t-type-code-" + lang_code).value = type_code;

        document.getElementById("t-type-value").innerText
            = document.getElementById("type-value-" + ui_lang_code + "-" + type_code).innerText.trim();

        document.getElementById("tutor-types-dropdown").classList.remove("active");
        document.getElementById("delete-type-button").style.display = "block";
        document.getElementById("type-editor-form-deleter").action =
            "/" + ui_lang_code + "/type/" + type_code + "/del";
    }
}

function changeBoundedTTypeAdmin(elem_id) {
    let type_code = elem_id.split("-").pop();
    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');
    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("bounded-t-type-code-" + lang_code).value = type_code;
    }
    document.getElementById("bounded-t-type-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("bounded-tutor-types-dropdown").classList.remove("active");
}


function addNewTTheme() {
    document.getElementById("t-theme-value").innerText = document.getElementById("t-theme-new").innerText.trim();
    document.getElementById("tutor-themes-dropdown").classList.remove("active");
    document.getElementById("delete-theme-button").style.display = "none";

    let theme_values = document.querySelectorAll('[id^="theme-value-"]');
    for (i=0; i<theme_values.length; i++) {
        theme_values[i].value = ""
    }

    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');
    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("submit-theme-button-" + lang_code).value =
            document.getElementById("add-new-button-value").innerText.trim();
        document.getElementById("theme-editor-form-" + lang_code).action =
            document.getElementById("theme-editor-form-default-value").value;
        document.getElementById("theme-lang-code-" + lang_code).value = lang_code;
        document.getElementById("t-theme-code-" + lang_code).value = "";
        document.getElementById("theme-editor-form-deleter").action = "";
        document.getElementById("bounded-t-type-code-" + lang_code).value = "";
    }
    document.getElementById("bounded-t-type-value").innerText =
        document.getElementById("bounded-t-type-default-value").innerText.trim();
}

function changeTThemeAdmin(elem_id, ui_lang_code, type_code) {
    let theme_code = elem_id.split("-").pop();
    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');

    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("theme-value-" + lang_code).value = "";
        try {
            document.getElementById("theme-value-" + lang_code).value =
                document.getElementById("theme-value-" + lang_code + "-" + theme_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("submit-theme-button-" + lang_code).value =
            (document.getElementById("theme-value-" + lang_code).value !== "")
                ? document.getElementById("save-button-value").innerText.trim()
                : document.getElementById("add-new-button-value").innerText.trim()

        document.getElementById("theme-editor-form-" + lang_code).action =
            "/" + ui_lang_code + "/theme/" + theme_code + "/edit";

        document.getElementById("theme-lang-code-" + lang_code).value = lang_code;

        document.getElementById("t-theme-code-" + lang_code).value = "";
        document.getElementById("t-theme-code-" + lang_code).value = theme_code;

        try {
            document.getElementById("t-theme-value").innerText
                = document.getElementById("theme-value-" + ui_lang_code + "-" + theme_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("tutor-themes-dropdown").classList.remove("active");
        document.getElementById("delete-theme-button").style.display = "block";
        document.getElementById("theme-editor-form-deleter").action =
            "/" + ui_lang_code + "/theme/" + theme_code + "/del";
        document.getElementById("bounded-t-type-code-" + lang_code).value = type_code;
    }
    try {
        document.getElementById("bounded-t-type-value").innerText =
            document.getElementById("bounded-t-type-" + type_code).innerText.trim();
    }
    catch (TypeError) {}
}

function addNewTDistType() {
    document.getElementById("t-dist-type-value").innerText = document.getElementById("t-dist-type-new").innerText.trim();
    document.getElementById("tutor-dist-types-dropdown").classList.remove("active");
    document.getElementById("delete-dist-type-button").style.display = "none";

    let dist_type_values = document.querySelectorAll('[id^="dist-type-value-"]');
    for (i=0; i<dist_type_values.length; i++) {
        dist_type_values[i].value = "";
    }

    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');
    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("submit-dist-type-button-" + lang_code).value =
            document.getElementById("add-new-button-value").innerText.trim();
        document.getElementById("dist-type-editor-form-" + lang_code).action =
            document.getElementById("dist-type-editor-form-default-value").value;
        document.getElementById("dist-type-lang-code-" + lang_code).value = lang_code;
        document.getElementById("t-dist-type-code-" + lang_code).value = "";
        document.getElementById("dist-type-editor-form-deleter").action = "";
    }
}

function changeTDistTypeAdmin(elem_id, ui_lang_code) {
    let dist_type_code = elem_id.split("-").pop();
    let ui_langs = document.querySelectorAll('[id^="ui-lang-"]');

    for (i=0; i<ui_langs.length; i++) {
        let lang_code = ui_langs[i].id.split("-").pop();
        document.getElementById("dist-type-value-" + lang_code).value = "";
        try {
            document.getElementById("dist-type-value-" + lang_code).value =
                document.getElementById("dist-type-value-" + lang_code + "-" + dist_type_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("submit-dist-type-button-" + lang_code).value =
            (document.getElementById("dist-type-value-" + lang_code).value !== "")
                ? document.getElementById("save-button-value").innerText.trim()
                : document.getElementById("add-new-button-value").innerText.trim()

        document.getElementById("dist-type-editor-form-" + lang_code).action =
            "/" + ui_lang_code + "/dist-type/" + dist_type_code + "/edit"

        document.getElementById("dist-type-lang-code-" + lang_code).value = lang_code;

        document.getElementById("t-dist-type-code-" + lang_code).value = "";
        document.getElementById("t-dist-type-code-" + lang_code).value = dist_type_code;

        document.getElementById("t-dist-type-value").innerText = ""
        try {
            document.getElementById("t-dist-type-value").innerText
                = document.getElementById("dist-type-value-" + ui_lang_code + "-" + dist_type_code).innerText.trim();
        }
        catch (TypeError) {}

        document.getElementById("tutor-dist-types-dropdown").classList.remove("active");
        document.getElementById("delete-dist-type-button").style.display = "block";
        document.getElementById("dist-type-editor-form-deleter").action =
            "/" + ui_lang_code + "/dist-type/" + dist_type_code + "/del";
    }
}

function addNewTLanguage() {
    document.getElementById("t-lang-value").innerText = document.getElementById("t-lang-new").innerText.trim();
    document.getElementById("tutorial-langs-dropdown").classList.remove("active");
    document.getElementById("delete-lang-button").style.display = "none";
    document.getElementById("tutorial-lang-code").value = "";
    document.getElementById("tutorial-lang-value").value = "";
    document.getElementById("submit-lang-button").value =
        document.getElementById("add-new-button-value").innerText.trim();
    document.getElementById("lang-editor-form").action =
        document.getElementById("lang-editor-form-default-value").value;
    document.getElementById("lang-editor-form-deleter").action = "";
}

function changeTLanguageAdmin(elem_id, ui_lang_code) {
    let lang_code = elem_id.split("-").pop();
    document.getElementById("tutorial-lang-code").value = lang_code;
    document.getElementById("tutorial-lang-value").value = document.getElementById(elem_id).innerText.trim();
    document.getElementById("t-lang-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("submit-lang-button").value =
            document.getElementById("save-button-value").innerText.trim();
    document.getElementById("lang-editor-form").action =
        "/" + ui_lang_code + "/lang/" + lang_code + "/edit";
    document.getElementById("tutorial-langs-dropdown").classList.remove("active");
    document.getElementById("delete-lang-button").style.display = "block";
    document.getElementById("lang-editor-form-deleter").action =
        "/" + ui_lang_code + "/lang/" + lang_code + "/del";
}
