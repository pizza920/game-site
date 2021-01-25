const friends = JSON.parse(document.getElementById('friends').textContent);
const preferences = JSON.parse(document.getElementById('preferences').textContent);
const userId = JSON.parse(document.getElementById('user_id').textContent);
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
const PREFERENCES_TITLE = "Invite People Like You";
const FRIENDS_TITLE = "Invite Friends";

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

function filterOutFriends(onlineUsers, friends) {
  return onlineUsers.filter(user => {
    return friends.some(friend => friend.id === user.id);
  });
}

const onlineUsersDiv = document.getElementById("online-users");
const inviteUsernameElement = document.getElementById("invite-username");
const filterTypeElement = document.getElementById("filter-type");

let friendsOnline = [];
let preferencedUsers = [];
let currentUsers = [];
let userSelected = null;


function createUserDiv(onlineUser) {
  const userDiv = document.createElement("div");
  userDiv.classList.add("online-user");
  userDiv.setAttribute("data-toggle", "modal");
  userDiv.setAttribute("data-target", "#send-invite-modal");
  userDiv.id = onlineUser.id;
  const userDivText = document.createElement("div");
  userDivText.classList.add("username");
  let usernameString = onlineUser.username;
  if (onlineUser.username.length > 12) {
    usernameString = onlineUser.username.substring(0, 12) + "...";
  }
  userDivText.innerHTML = usernameString;
  const userImage = document.createElement("img");
  userImage.classList.add("profile-picture");
  if (typeof (onlineUser.picture) === "string" && onlineUser.picture.length > 0) {
    userImage.src = onlineUser.picture;
  }
  const inviteButton = document.createElement("div");
  inviteButton.classList.add("invite-user-button");
  inviteButton.innerHTML = "Invite";
  inviteButton.onclick = function () {
    userSelected = onlineUser;
    inviteUsernameElement.textContent = onlineUser.username;
  };
  userDiv.appendChild(userImage);
  userDiv.appendChild(userDivText);
  userDiv.appendChild(inviteButton);
  return userDiv;
}

function setUsersBasedOnFilter(filter) {
  if (filter === PREFERENCES) {
    currentUsers = preferencedUsers;
    filterTypeElement.textContent = PREFERENCES_TITLE;
  } else {
    currentUsers = friendsOnline;
    filterTypeElement.textContent = FRIENDS_TITLE;
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
  const usersFilteredByPreferences = filterByPreferences(data.online_users);
  friendsOnline = filterOutFriends(data.online_users, friends);
  preferencedUsers = usersFilteredByPreferences;
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