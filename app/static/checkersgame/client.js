var socketisready = false;
socketisready = false;

var execInUnity = function(method) {
    if (!socketisready) return;
    var args = Array.prototype.slice.call(arguments, 1);
    unityInstance.SendMessage("MainLobby", method, args.join(','));
};

var createFriendRoom = function(){
    if (!socketisready) return;
    unityInstance.SendMessage("MainLobby",'CreateFriendRoom');
}

var joinFriendRoom = function(){
    if(!socketisready) return;
    unityInstance.SendMessage("MainLobby",'JoinFriendRoom');
}

var RandomMatching = function(){
    if(!socketisready) return;
    unityInstance.SendMessage("MainLobby",'OnClickRandomButton');
}

var ExitGame = function(){
    location.reload();
}
window.addEventListener('load', function() {
	
	
	var update = function() {
		// unityInstance.SendMessage("Player", "Talk", '@' + name + ': ' + message);
	};

});

// <!DOCTYPE html>
// <html lang="en-us">
//   <head>
// 	<meta charset="utf-8">
// 	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
// 	<title>RNGod</title>
// 	<link rel="shortcut icon" href="TemplateData/favicon.ico">
// 	<link rel="stylesheet" href="TemplateData/style.css">
// 	<script src="TemplateData/UnityProgress.js"></script>
// 	<script src="Build/UnityLoader.js"></script>
// 	<script src= "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"> </script> 
// 	<script> 
// 		setCookie("ip", "none", 1000);
// 	 $.getJSON("https://api.ipify.org?format=json",function(data) { 
// 		 setCookie("ip", data.ip, 1000);
// 		 console.log("AA",data.ip);
// 	 }) 
// 	 function setCookie(cname, cvalue, exdays) {
// 	   var d = new Date();
// 	   d.setTime(d.getTime() + (exdays*24*60*60*1000));
// 	   var expires = "expires="+ d.toUTCString();
// 	   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
// 	 }
	 
//  </script> 
   
// 	<script>
// 	  var unityInstance = UnityLoader.instantiate("unityContainer", "Build/webgl_rngod.json", {onProgress: UnityProgress});
// 	</script>
// 	<script src="/socket.io/socket.io.js"></script>
//   </head>
//   <body>
// 	<div class="webgl-content">
// 	  <div id="unityContainer" style="width: 100%; height: 100%"></div>
// 	</div>
// 	<script src="./client.js"></script>
//   </body>
// </html>


// .webgl-content * {border: 0; margin: 0; padding: 0}
// .webgl-content { position: absolute; width: 100%;height: 100%;}
// .webgl-content .logo, .progress {position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%);}
// .webgl-content .logo {background: url('progressLogo.Light.png') no-repeat center / contain; width: 154px; height: 130px;display: none;}
// .webgl-content .progress {height: 18px; width: 141px; margin-top: 90px;}
// .webgl-content .progress .empty {background: url('progressEmpty.Light.png') no-repeat right / cover; float: right; width: 100%; height: 100%; display: inline-block;}
// .webgl-content .progress .full {background: url('progressFull.Light.png') no-repeat left / cover; float: left; width: 0%; height: 100%; display: inline-block;}

// .webgl-content .logo.Dark {background-image: url('progressLogo.Dark.png');display: none;}
// .webgl-content .progress.Dark .empty {background-image: url('progressEmpty.Dark.png');}
// .webgl-content .progress.Dark .full {background-image: url('progressFull.Dark.png');}

// .webgl-content .footer {margin-top: 5px; height: 38px; line-height: 38px; font-family: Helvetica, Verdana, Arial, sans-serif; font-size: 18px;}
// .webgl-content .footer .webgl-logo, .title, .fullscreen {height: 100%; display: inline-block; background: transparent center no-repeat;}
// .webgl-content .footer .webgl-logo {background-image: url('webgl-logo.png'); width: 204px; float: left;}
// .webgl-content .footer .title {margin-right: 10px; float: right;}
// .webgl-content .footer .fullscreen {background-image: url('fullscreen.png'); width: 38px; float: right;}
