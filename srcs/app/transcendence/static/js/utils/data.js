export function dataForm(fields)
{
	let data = new FormData();

	fields.forEach(field => {
		let element = document.getElementById(field);
		if (element) {
			let value;
			if (field === 'avatar') {
				const file = element.files[0];
				if (file.size > 1000000) {
					console.log('Image size exceeds the limit (maximal size: 1MB)');
					return null;
				}
				value = file;
			}
			else {
				value = element.value;
			}
			data.append(field, value);
		}
		else {
			console.log(`Element with ID ${field} not found`);
		}
	});

	return data;
}