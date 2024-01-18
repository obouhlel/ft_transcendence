import { getElt, resizeMain } from './utils.js';
import { route } from './route.js';

export const main = getElt('main');

resizeMain();
route();
window.addEventListener('resize', () => resizeMain(main));
window.addEventListener('popstate', route);