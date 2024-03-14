import { handleLoginFormSubmit } from './form/login.js';
import { handleRegisterFormSubmit } from './form/register.js';
import { handleEditProfileFormSubmit } from './form/edit_profile.js';
import { show_dynamic_friends, deleteFriend, searchFunction, addFriendHandler, openModal } from './profile/friends.js';
import { show_dynamic_stats, show_dynamic_history } from './profile/stats.js';
import { switchGameTab, friendsTab } from './profile/tabs.js';
import { handleLogout } from './utils/logout.js';
import { changeAvatar } from './utils/avatar.js';
import { message } from './utils/message.js'; // Added import statement
import { matchmacking } from './games/matchmaking.js';
import { pong3D } from './games/pong/pong.js';
import { ticTacToe3D } from './games/ticTacToe/ticTacToe.js';
import { fetchUserDataAndRenderChart, fetchUserDataAndProcessAges, updateDashboardDisplay, setupTabEventListeners} from './dashboard.js';
import { tournamentHandler, createTournamentHandler } from './games/tournament.js';
import { GameHandler } from './games/game.js';

export function handleGameRequest(gameId) {
    switch(gameId) {
        case '1':
            return matchmacking('pong');
        case '2':
            return matchmacking('ticTacToe');
        default:
            console.error('Unknown game id');
    }
}

export const pageHandlers = {
    '400': [message],
    'login': [handleLoginFormSubmit],
    'register': [handleRegisterFormSubmit, changeAvatar],
    'dashboard': [setupTabEventListeners, fetchUserDataAndRenderChart, fetchUserDataAndProcessAges, () => updateDashboardDisplay(1)],
    'profile': [show_dynamic_friends, openModal, addFriendHandler, searchFunction,
                () => show_dynamic_history(1), () => show_dynamic_stats(1), friendsTab,
                switchGameTab, deleteFriend],
    'edit_profile': [handleEditProfileFormSubmit, changeAvatar],
    'game': [gameId => handleGameRequest(gameId)],
    'pong': [pong3D],
    'TicTacToe': [ticTacToe3D],
    'tournament': [tournamentHandler],
    'create-tournament': [createTournamentHandler],
};
