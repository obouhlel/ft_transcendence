import { doRequest } from "./utils/fetch.js";

export function test() {
    console.log('Test GETS');
    const response = doRequest.get('/api/games/');
    console.log(response);
}