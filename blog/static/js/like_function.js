function likeArticle(articleId){
    const likeCount = document.getElementById(`likes-count-${articleId}`);
    const likeButton = document.getElementById(`likes-button-${articleId}`);

    fetch(`/article/${articleId}/like`, {method:"POST"})
    .then((res)=> res.json()).then((data)=>{
        likeCount.innerHTML = data["likes"];
        console.log(data['liked'])
        if (data["liked"] === true){
            likeButton.class = 'fas fa-thumbs-up fa-2x'; 
            console.log(data['liked'])
        }else{
            likeButton.class = 'far fa-thumbs-up fa-2x'; 
            console.log(data['liked'])

        }
    });
};