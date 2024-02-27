export function dataForm(fields)
{
	let data = new FormData();

	fields.forEach(field => {
		let element = document.getElementById(field);
		if (element) {
			let value = field === 'avatar' ? element.files[0] : element.value;
			data.append(field, value);
		}
		else {
			console.log(`Element with ID ${field} not found`);
		}
	});

	return data;
}