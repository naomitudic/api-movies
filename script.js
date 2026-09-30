const API_URL = "http://127.0.0.1:8000";

async function getJSON(path, options = {}) {
    const res = await fetch(`${API_URL}${path}`, options);
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const detail = Array.isArray(body.detail)
            ? body.detail.map(d => d.msg).join(", ")
            : body.detail;
        throw new Error(detail || `${path} devolvió ${res.status}`);
    }
    return res.json();
}

function fillSelect(select, items, placeholder) {
    select.replaceChildren();
    if (placeholder) {
        select.append(new Option(placeholder, ""));
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

        fillSelect(document.getElementById("directorSelect"), directors, "Seleccionar director");
        fillSelect(document.getElementById("genreSelect"), genres);
    } catch (error) {
        console.error("Error al cargar las selecciones:", error);
    }
}

function createMovieCard(movie) {
    const card = document.createElement("article");
    card.className = "movie-card";

    const title = document.createElement("h3");
    title.textContent = `${movie.id}. ${movie.title}`;
    card.append(title);

    const meta = document.createElement("p");
    const available = movie.is_available ? "Disponible" : "No disponible";
    meta.textContent = `${movie.year} · ${movie.duration} min · ${available}`;
    card.append(meta);

    const director = document.createElement("p");
    director.textContent = `Director: ${movie.director ? movie.director.name : "—"}`;
    card.append(director);

    const genres = document.createElement("ul");
    genres.className = "genres";
    for (const genre of movie.genres ?? []) {
        const item = document.createElement("li");
        item.textContent = genre.name;
        genres.append(item);
    }
    card.append(genres);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "delete";
    remove.textContent = "Eliminar";
    remove.addEventListener("click", () => deleteMovie(movie.id));
    card.append(remove);

    return card;
}

async function loadMovies() {
    const list = document.getElementById("movieList");
    try {
        const movies = await getJSON("/movie/");
        list.replaceChildren();
        for (const movie of movies) {
            list.append(createMovieCard(movie));
        }
    } catch (error) {
        console.error("Error al cargar películas:", error);
        list.textContent = `No se pudieron cargar las películas: ${error.message}`;
    }
}

async function deleteMovie(id) {
    if (!confirm(`¿Eliminar la película ${id}?`)) return;

    try {
        await getJSON(`/movie/${id}`, { method: "DELETE" });
        await loadMovies();
    } catch (error) {
        console.error("Error al eliminar:", error);
        alert(`No se pudo eliminar: ${error.message}`);
    }
}

document.getElementById("movieForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const form = event.currentTarget;
    const errorBox = document.getElementById("formError");
    const submitBtn = document.getElementById("submitBtn");

    errorBox.hidden = true;
    submitBtn.disabled = true;

    const selectedGenres = Array.from(
        document.getElementById("genreSelect").selectedOptions,
        opt => parseInt(opt.value, 10)
    );
    const directorValue = document.getElementById("directorSelect").value;

    const payload = {
        title: document.getElementById("title").value.trim(),
        duration: parseInt(document.getElementById("duration").value, 10),
        year: parseInt(document.getElementById("year").value, 10),
        director_id: directorValue ? parseInt(directorValue, 10) : null,
        genre_ids: selectedGenres,
        is_available: document.getElementById("isAvailable")?.checked ?? true
    };

    try {
        await getJSON("/movie/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        form.reset();
        await loadMovies();
    } catch (error) {
        errorBox.textContent = error.message;
        errorBox.hidden = false;
    } finally {
        submitBtn.disabled = false;
    }
});

loadSelectOptions();
loadMovies();
