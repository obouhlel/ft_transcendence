import { doRequest } from "../utils/fetch.js";

export function aliasFormsHandler() {
	const aliasForms = document.getElementById("alias-forms");
	if (!aliasForms)
		return;
		// return console.error('Element with id "alias-forms" not found');
	const handleSubmit = (event) => {
		event.preventDefault();

		const alias = document.getElementById("alias").value;
		const data = { alias: alias };
		doRequest.post(`/api/alias/`, data, (response) => {
			const messageElement = document.getElementById("message");
			if (!messageElement)
				return;
				// return console.error('Element with class "message" not found');
			if (response.status === "ok") {
				messageElement.textContent = response.message;
			} else if (response.status === "error") {
				messageElement.textContent = response.message;
			}
		});
	};
	aliasForms.addEventListener("submit", handleSubmit);
}
