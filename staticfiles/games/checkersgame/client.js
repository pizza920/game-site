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
