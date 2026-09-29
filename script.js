const API_URL = "http://127.0.0.1:8000"

async function loadSelectOptions() {
    try {
        const [DirectorResponse, GenreResponse] = await Promise.all([
            fetch(`${API_URL}/director/`),
            fetch(`${API_URL}/genre/`)
        ]);

        const director = await DirectorResponse.json()
        const genre = await GenreResponse.json()

        const DirectorSelect = document.getElementById("DirectorSelect");
        director.forEach(d => {
            DirectorSelect.innerHTML += `<option value="{d.id}">${d.name}<option`
        })

}