import { pageHandlers, pageHandlersNotLoggedIn } from "./pages.js";
import { handleLoginFormSubmit } from "./form/login.js";
import { handleLogout } from "./utils/logout.js";
import { dropdown, responsiveNav } from "./header.js";
import { searchFunction } from "./profile/friends.js";
import {
  handlerNotification,
  handleNotificationVisual,
  handlerNotificationAction,
} from "./notifs.js";
import { doRequest, getCookie } from "./utils/fetch.js";

let isNotificationHandled = false;
window.clean = [];

window.addEventListener("hashchange", function () {
  window.clean.forEach((func) => func());
  window.clean = [];
  let [page, params] = hashChangeHandler();
  window.searchFunction = searchFunction;
  showPage(page, params);
});

window.addEventListener("load", function () {
  window.clean.forEach((func) => func());
  window.clean = [];
  let [page, params] = hashChangeHandler();
  window.searchFunction = searchFunction;
  showPage(page, params);
});

export function hashChangeHandler() {
  let hash = window.location.hash.substring(1);
  let [page, params] = hash.split("?");

  page = page || "home";

  return [page, params];
}

function is_logged_in() {
  const is_logged_in = document.getElementById("logout-button");
  if (is_logged_in) return true;
  return false;
}

export async function executeHandlers(page) {
  for (const func of pageHandlers[page]) {
    const res = await func();
    if (typeof res === "function") {
      window.clean.push(res);
    }
  }
}

function executeHandlersNotLoggedIn(page) {
  if (!pageHandlersNotLoggedIn[page]) return;
  for (const func of pageHandlersNotLoggedIn[page]) {
    func();
  }
}

async function showPage(page, params) {
  const data_header = await doRequest.get(`/update_header/${page}/`);
  const header_content = document.getElementById("header");
  header_content.innerHTML = data_header.html;

  const isLogged = is_logged_in();

  const data_page = await doRequest.get(`/pages/${page}${params ? "?" + params : ""}`);
  const page_content = document.getElementById("page");
  page_content.innerHTML = data_page.html;

  if (!isLogged) executeHandlersNotLoggedIn(page);
  else if (pageHandlers[page]) executeHandlers(page);

  if (isLogged) {
    handleLogout();
    responsiveNav();
    dropdown();
    handleNotificationVisual();
    handlerNotificationAction();
    if (!isNotificationHandled) {
      handlerNotification();
      isNotificationHandled = true;
    }
  }
  if (!isLogged) isNotificationHandled = false;
}
