$(document).ready(function() {
  $('body').tooltip({ selector: '[data-toggle="tooltip"]' });
});

const friends = JSON.parse(document.getElementById('friends').textContent);
const preferences = JSON.parse(document.getElementById('preferences').textContent);
const userId = JSON.parse(document.getElementById('user_id').textContent);

console.log("FRIENDS: ", friends);
const wsScheme = window.location.protocol == "https:" ? "wss://" : "ws://";
const allUsersSocket = new WebSocket(
  wsScheme
  + window.location.host
  + '/ws/chat/1/'
);
const inviteSocket = new WebSocket(
  wsScheme
  + window.location.host
  + '/ws/send-game-invite/' + userId + '/'
);
const PREFERENCES = 'PREFERENCES';
const FRIENDS = 'FRIENDS';
let filter = PREFERENCES;
const PREFERENCES_TITLE = "People Like You";
const FRIENDS_TITLE = "Friends";

function filterByPreferences(onlineUsers) {
  const usersToShow = onlineUsers.filter(user => {
    for (let key in preferences) {
      let preference = preferences[key];
      if (preference !== null && preference !== undefined) {
        if (user[key] !== preference) return false;
      }
    }
    return true;
  });
  return usersToShow;
}

function getFriendsWithStatus(onlineUsers, friends) {
  return friends.map(friend => {
    const friendCopy = Object.assign({}, friend);
    if (onlineUsers.some(onlineUser => onlineUser.id === friend.id)) {
      friendCopy.onlineStatus = true;
    } else {
      friendCopy.onlineStatus = false;
    }
    return friendCopy;
  });
}

const onlineUsersDiv = document.getElementById("online-users");
const inviteUsernameElement = document.getElementById("invite-username");
const filterTypeElement = document.getElementById("filter-type");
const peopleLinkElement = document.getElementById("people-link");

let friendsOnline = [];
let preferencedUsers = [];
let currentUsers = [];
let userSelected = null;

function createStatusDiv(onlineStatus) {
  const statusDiv = document.createElement("div");
  statusDiv.classList.add("dot");
  if (onlineStatus === true) {
    statusDiv.classList.add("online");
  } else {
    statusDiv.classList.add("offline");
  }
  return statusDiv;
}

function createUserDiv(onlineUser) {
  const userDiv = document.createElement("div");
  userDiv.classList.add("online-user");
  userDiv.setAttribute("data-toggle", "modal");
  userDiv.setAttribute("data-target", "#send-invite-modal");
  userDiv.id = onlineUser.id;
  const userImage = document.createElement("img");
  userImage.classList.add("profile-picture");
  userImage.setAttribute("data-toggle", "tooltip");
  const tooltipText = "Click to call " + onlineUser.username;
  userImage.setAttribute("title", tooltipText);
  if (typeof (onlineUser.picture) === "string" && onlineUser.picture.length > 0) {
    userImage.src = onlineUser.picture;
  }
  userImage.onclick = function () {
    userSelected = onlineUser;
    inviteUsernameElement.textContent = onlineUser.username;
  };
  // If it has this property it is filtered by friends and needs to have extra element to display status
  if (typeof(onlineUser.onlineStatus) === "boolean") {
    userDiv.appendChild(userImage);
    userDiv.appendChild(createStatusDiv(onlineUser.onlineStatus));
    if (onlineUser.onlineStatus === true) userDiv.appendChild(inviteButton);
  //  On preferenced users
  } else {
    userDiv.appendChild(userImage);
  }
  return userDiv;
}

function setUsersBasedOnFilter(filter) {
  if (filter === PREFERENCES) {
    currentUsers = preferencedUsers;
    filterTypeElement.textContent = PREFERENCES_TITLE;
    peopleLinkElement.classList.remove("hide");
  } else {
    currentUsers = friendsOnline;
    filterTypeElement.textContent = FRIENDS_TITLE;
    peopleLinkElement.classList.add("hide");
  }
  console.log("CURRENT USERS: ", currentUsers);
  onlineUsersDiv.textContent = '';

  currentUsers.forEach(onlineUser => {
    onlineUsersDiv.appendChild(createUserDiv(onlineUser));
  });
}

function sendUserInvite() {
  inviteSocket.send(JSON.stringify({user: userSelected, type: "send_invite"}));
}

allUsersSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  friendsOnline = getFriendsWithStatus(data.online_users, friends);
  preferencedUsers = filterByPreferences(data.online_users);
  setUsersBasedOnFilter(filter);
};

allUsersSocket.onclose = function (e) {
  console.error('Chat socket closed unexpectedly');
};

allUsersSocket.onopen = function (e) {
};

const generateToastMessage = function (message) {
  const acceptHtml = '<div><a href="#">Accept</a></div>';
  const declineHtml = '<div><a href="#">Decline</a></div>';
  return (
    message + '\n' +
    acceptHtml + '\n' +
    declineHtml
  )
}


inviteSocket.onmessage = function (e) {
  toastr.options.positionClass = 'toast-bottom-left';
  const data = JSON.parse(e.data);
  toastr.info(generateToastMessage(data.message));
}


const hideShowButton = document.getElementById('hideShowButton');
const onlineUserBox = document.getElementById('online-user-box');
let hidden = false;

function hideShow(e) {
  if (hidden) {
    hideShowButton.classList.remove('fa-plus');
    hideShowButton.classList.add('fa-minus');
    onlineUserBox.classList.remove('hidden');
    onlineUsersDiv.classList.remove('hide');
  } else {
    hideShowButton.classList.remove('fa-minus');
    hideShowButton.classList.add('fa-plus');
    onlineUserBox.classList.add('hidden');
    onlineUsersDiv.classList.add('hide');
  }
  hidden = !hidden;
}

const onlineUsersToggle = document.getElementById('online-users-toggle');

function toggleOnlineUsers() {
  if (filter === FRIENDS) {
    onlineUsersToggle.classList.remove("fa-user-friends");
    onlineUsersToggle.classList.add("fa-user");
    filter = PREFERENCES;
  } else {
    onlineUsersToggle.classList.remove("fa-user");
    onlineUsersToggle.classList.add("fa-user-friends");
    filter = FRIENDS;
  }
  setUsersBasedOnFilter(filter);
}