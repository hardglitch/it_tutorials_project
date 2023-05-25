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

function changeTType(elem_id) {
    document.getElementById("t-type-value").innerText = document.getElementById(elem_id).innerText.trim();
    let type_code = elem_id.split("-")[2]
    document.getElementById("t-type-code").value = type_code
    document.getElementById("tutor-types-dropdown").classList.remove("active");
    getAllowedThemes(type_code)
}

function changeTTheme(elem_id) {
    document.getElementById("t-theme-value").innerText = document.getElementById(elem_id).innerText.trim();
    document.getElementById("t-theme-code").value = elem_id.split("-").pop();
    document.getElementById("tutor-themes-dropdown").classList.remove("active");
}

function getAllowedThemes(type_code = undefined, set_default_theme = true) {
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
        if (divs[i].id.startsWith("inherit-from-type-code-" + type_code)) {
            if (first === false && set_default_theme === true) {
                changeTTheme(divs[i].id)
                first = true
            }
            divs[i].style.display = ""
        }
    }
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
