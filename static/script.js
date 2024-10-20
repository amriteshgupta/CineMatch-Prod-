// script.js
document.getElementById('getMovieButton').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default button behavior

    // Fetch a new movie
    const yearInput = document.getElementById('year');
    const genreInput = document.getElementById('genre');

    const year = yearInput.value;
    const genre = genreInput.value;

    console.log(`Fetching movie with year: ${year}, genre: ${genre}`);  // Add this line

    fetch(`/api/movie?year=${year || ''}&genre=${genre || ''}`)
        .then(response => {
            if (!response.ok) {
                console.error(`HTTP error! status: ${response.status}`);  // Log HTTP errors
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Movie data received:', data);  // Log the received movie data
            if (data.title) {
                document.querySelector('h1').innerText = data.title;
                document.querySelector('.movie-poster').src = data.poster_path || '';
                document.querySelector('p:nth-of-type(1)').innerHTML = `<strong>Release Date:</strong> ${data.release_date || 'N/A'}`;
                document.querySelector('p:nth-of-type(2)').innerText = data.overview || 'No overview available.';
            } else {
                alert('No movie found! Please try different filters.');
            }
        })
        .catch(error => console.error('There was a problem with the fetch operation:', error));
});
