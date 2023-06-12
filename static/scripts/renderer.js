/*
 *
 *   JS script 
 *    renderer.js Pre-alpha version
 *
 *    This script renders YouTube video players based on the provided video ids.
 *    Arturo Olivares
 *
 *    Copyright (C) 2023 Arturo Olivares
 *    GNU GPLv3
 *
**/

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var players = [];

function onYouTubeIframeAPIReady() {
  var videoIds = [
    document.getElementById("latest-video").textContent,
    document.getElementById("popular-video").textContent,
    document.getElementById("oldest-video").textContent
  ];

  for (var i = 0; i < videoIds.length; i++) {
    players[i] = new YT.Player('player' + (i + 1), {
      height: '100%',
      width: '40%',
      videoId: videoIds[i],
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }
    });
  }
}

function onPlayerReady(event) {
  event.target.playVideo();
}

var done = false;

function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideos, 6000);
    done = true;
  }
}

function stopVideos() {
  for (var i = 0; i < players.length; i++) {
    players[i].stopVideo();
  }
}