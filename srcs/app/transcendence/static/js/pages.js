import { handleLoginFormSubmit } from "./form/login.js";
import { handleRegisterFormSubmit } from "./form/register.js";
import { handleRegister42FormSubmit } from "./form/register_42.js";
import { handleEditProfileFormSubmit } from "./form/edit_profile.js";
import {
  show_dynamic_friends,
  deleteFriend,
  searchFunction,
  addFriendHandler,
  openModal,
} from "./profile/friends.js";
import { show_dynamic_stats, show_dynamic_history } from "./profile/stats.js";
import { switchGameTab, friendsTab } from "./profile/tabs.js";
import { changeAvatar } from "./utils/avatar.js";
import { message } from "./utils/message.js";
import { pong3D } from "./games/pong/pong.js";
import { ticTacToe3D } from "./games/ticTacToe/ticTacToe.js";
import {
  fetchUserDataAndRenderChart,
  fetchUserDataAndProcessAges,
  updateDashboardDisplay,
  setupTabEventListeners,
} from "./dashboard.js";
import {
  tournamentHandler,
  createTournamentHandler,
  aliasFormsHandler,
  tournamentLobbyHandler,
} from "./games/tournament.js";
import { GameHandler } from "./games/game.js";

export const pageHandlers = {
  400: [message],
  login: [handleLoginFormSubmit],
  register: [handleRegisterFormSubmit, changeAvatar],
  "register-42": [handleRegister42FormSubmit, changeAvatar],
  dashboard: [
    setupTabEventListeners,
    fetchUserDataAndRenderChart,
    fetchUserDataAndProcessAges,
    () => updateDashboardDisplay(1),
  ],
  profile: [
    show_dynamic_friends,
    openModal,
    addFriendHandler,
    searchFunction,
    () => show_dynamic_history(1),
    () => show_dynamic_stats(1),
    friendsTab,
    switchGameTab,
    deleteFriend,
  ],
  edit_profile: [handleEditProfileFormSubmit, changeAvatar],
  game: [GameHandler], // Added 'game' page handler
  pong: [pong3D],
  tictactoe: [ticTacToe3D],
  tournament: [tournamentHandler, aliasFormsHandler],
  "create-tournament": [createTournamentHandler],
  "lobby-tournament": [tournamentLobbyHandler],
};
