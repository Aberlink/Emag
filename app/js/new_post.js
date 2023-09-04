const articleForm = document.getElementById('article-form');

const username = localStorage.getItem('username');
const password = localStorage.getItem('password');

const auth = 'Basic ' + btoa(username + ':' + password);

articleForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = event.target.title.value;
    const author = event.target.author.value;
    const content = event.target.content.value;

    const reqyestBody = {
        title: title,
        author: author,
        content: content,
    };

    const response = await fetch('http://localhost:8000/api/v1/article/', {
        method: 'POST',
        headers: {
            'Authorization': auth,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(reqyestBody),
    });

    if (response.status === 201) {
        console.log('Article created successfully');
        window.location.reload();
    } else {
        console.error('Failed to create article');
    }
});