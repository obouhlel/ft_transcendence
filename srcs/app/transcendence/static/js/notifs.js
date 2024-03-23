import { doRequest } from "./utils/fetch.js";
import { handleLogout } from "./utils/logout.js";
import { dropdown, responsiveNav } from "./header.js";
import { show_dynamic_friends } from "./profile/friends.js";
import { hashChangeHandler } from "./load.js";

export async function handlerNotification() {
  // setup chat scoket
  const notifyScoket = new WebSocket(
    "wss://" + window.location.host + "/ws/notify/"
  );

  // on socket open
  notifyScoket.onopen = function (e) {
    console.log("Socket notify connected.");
  };

  // on socket close
  notifyScoket.onclose = function (e) {
    console.log("Socket notify closed unexpectedly");
  };

  // on receiving message on group
  notifyScoket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const pages = hashChangeHandler();

    if (message === "Send") {
      updateHeader();
    }
    if (message === "Accepted" && pages[0] === "profile") {
      console.log("Friend request accepted");
      show_dynamic_friends();
    }
  };

  // Listen for hash changes
  window.addEventListener("hashchange", function () {
    const pageNoNotification = ["login", "register"];
    const currentHash = window.location.hash.substring(1);
    if (pageNoNotification.includes(currentHash)) {
      notifyScoket.close();
    }
  });
}

async function updateHeader() {
  const header = document.getElementById("header");
  const pages = hashChangeHandler();
  const data = await doRequest.get(`/update_header/${pages[0]}/`);
  header.innerHTML = data.html;
  handleNotificationVisual();
  handlerNotificationAction();
  handleLogout();
  responsiveNav();
  dropdown();
  if (pages[0] === "profile") {
    show_dynamic_friends();
  }
}

export function handleNotificationVisual() {
  let count = document.querySelectorAll(".notif").length;
  if (count > 0) {
    const bellBtn = document.querySelector(".bell-btn");
    bellBtn.classList.add("show-notification");
  } else {
    const bellBtn = document.querySelector(".bell-btn");
    bellBtn.classList.remove("show-notification");
  }
}

export function handlerNotificationAction() {
  const notificationElements = document.querySelectorAll('[id^="notif-"]');
  notificationElements.forEach((element) => {
    const id = element.id.split("-")[1];
    const acceptElement = document.getElementById(`accept-${id}`);
    const denyElement = document.getElementById(`deny-${id}`);

    acceptElement.addEventListener("click", () => {
      // send accept friendrequest
      const data = {
        request_id: id,
        action: "accept",
      };
      doRequest.post("/api/respond_friend_request/", data, updateHeader);
      console.log(`Accept clicked for notification ${id}`);
    });

    denyElement.addEventListener("click", () => {
      // send deny friendrequest
      const data = {
        request_id: id,
        action: "decline",
      };
      doRequest.post("/api/respond_friend_request/", data, updateHeader);
      console.log(`Deny clicked for notification ${id}`);
    });
  });
}
