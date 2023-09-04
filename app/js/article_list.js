const articleListElement = document.getElementById('article-list');
        fetch('http://localhost:8000/api/v1/article/') 
            .then(response => response.json())
            .then(data => {
                data.forEach(article => {
                    const listItem = document.createElement('li');
                    const link = document.createElement('a');
                    link.textContent = article.title;
                    link.href = `article_details.html?id=${article.id}`;
                    listItem.appendChild(link);
    
                    const authorText = document.createTextNode(`, Author: ${article.author_email}`);
                    listItem.appendChild(authorText);
    
                    articleListElement.appendChild(listItem);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });