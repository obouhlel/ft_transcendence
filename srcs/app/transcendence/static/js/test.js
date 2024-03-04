import { doRequest } from "./utils/fetch.js";

export async function test() {
    console.log('Test GETS');
    const get_all_users = await doRequest.get(`/api/get_all_users/`);
    console.log(get_all_users.users);
    const get_user_name = await doRequest.get(`/api/get_user_name/`);
    console.log(get_user_name);
    const get_user_by_username = await doRequest.get(`/api/get_user_by_username/user2`);
    console.log(get_user_by_username);
    const get_user_by_id = await doRequest.get(`/api/get_user_by_id/1`);
    console.log(get_user_by_id);
}