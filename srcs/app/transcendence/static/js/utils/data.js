export function dataForm(fields)
{
	let data = new FormData();
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
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
	
	if (!csrftoken)
	{
		console.error('CSRF token not found');
		return data;
	}
	
	data.append('csrfmiddlewaretoken', csrftoken);
	return data;
}