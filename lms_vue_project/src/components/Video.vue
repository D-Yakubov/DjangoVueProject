<template>
    <div class="video-container">
        <iframe 
            :src="'https://www.youtube.com/embed/' + youtube_id"
            width="1100" 
            height="600" 
            frameborder="0" 
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;" 
            allowfullscreen
        ></iframe>
    </div>
    </template>
    
    <script>
    export default {
        props: ['youtube_id']
    }
    </script>