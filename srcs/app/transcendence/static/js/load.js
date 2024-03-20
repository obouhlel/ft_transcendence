import { pageHandlers } from "./pages.js";
import { handleLoginFormSubmit } from "./form/login.js";
import { handleLogout } from "./utils/logout.js";
import { dropdown, responsiveNav } from "./header.js";
import { searchFunction } from "./profile/friends.js";
import {
  handlerNotification,
  handleNotificationVisual,
  handlerNotificationAction,
} from "./notifs.js";
import { doRequest } from "./utils/fetch.js";

let isNotificationHandled = false;
let dashboardButtonSetup = false;
window.clean = [];

function setupDashboardButton() {
  if (dashboardButtonSetup) return;

  const navBtns = document.querySelector('.nav-btns');
  if (!navBtns) {
    console.error('Navigation buttons container not found.');
    return;
  }

  console.log('Setting up dashboard button...');
  console.log('Nav buttons container:', navBtns);

  navBtns.addEventListener('click', function(event) {
    const target = event.target;
    console.log('Clicked element:', target);
    if (target.classList.contains('btn-dashboard')) {
      event.preventDefault();
      const btnGamepad = document.querySelector('.btn-gamepad');
      if (!btnGamepad) {
        console.error('Gamepad button not found.');
        return;
      }
      const btnDashboard = target;
      console.log('Dashboard button:', btnDashboard);
      console.log('Gamepad button:', btnGamepad);
      btnGamepad.querySelector('img').src = btnGamepad.querySelector('img').getAttribute('data-src');
      btnDashboard.querySelector('img').src = btnDashboard.querySelector('img').getAttribute('data-src');
    }
  });

  dashboardButtonSetup = true;
}


window.addEventListener("hashchange", function () {
  // Remove all event listeners
  window.clean.forEach((func) => func());
  window.clean = [];
  let [page, params] = hashChangeHandler();
  window.searchFunction = searchFunction;
  showPage(page, params);

  if (page === 'dashboard') {
    setupDashboardButton();
  }
});

window.addEventListener("load", function () {
  let [page, params] = hashChangeHandler();
  window.searchFunction = searchFunction;
  showPage(page, params);

  if (page === 'dashboard') {
    setupDashboardButton();
  }
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

async function executeHandlers(page) {
  for (const func of pageHandlers[page]) {
    const res = await func();
    if (typeof res === "function") {
      window.clean.push(res);
    }
  }
}

async function showPage(page, params) {
  const data_header = await doRequest.get(`/update_header/`);
  const header_content = document.getElementById("header");
  header_content.innerHTML = data_header.html;

  const data_page = await doRequest.get(
    `/pages/${page}${params ? "?" + params : ""}`
  );
  const page_content = document.getElementById("page");
  page_content.innerHTML = data_page.html;
  const isLogged = is_logged_in();
  if (!isLogged && page === "home") handleLoginFormSubmit();
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
