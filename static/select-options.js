const API_URL = "http://127.0.0.1:8000";

async function getJSON(path) {
    const res = await fetch(`${API_URL}${path}`);
    if (!res.ok) {
        throw new Error(`${path} devolvio ${res.status}`);
    }
    return res.json();
}

function fillSelect(select, items, { allLabel } = {}) {
    select.replaceChildren();
    if (allLabel) {
        select.append(new Option(allLabel, ""));
    }
    for (const item of items) {
        select.append(new Option(item.name, String(item.id)));
    }
}

async function loadSelectOptions() {
    try {
        const [directors, genres] = await Promise.all([
            getJSON("/director/"),
            getJSON("/genre/")
        ]);

        fillSelect(document.getElementById("DirectorSelect"), directors, {
            allLabel: "-- Sin director --"
        });
        fillSelect(document.getElementById("GenreSelect"), genres);
    } catch (error) {
        console.error("No se pudieron cargar las listas:", error);
    }
}
