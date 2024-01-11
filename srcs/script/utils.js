export function getElt(selector)
{
	if (!selector)
		return null;
	else
		return document.querySelector(selector);
}

export function createElt(tag, className, textContent)
{
	const element = document.createElement(tag);
	if (className)
		element.classList.add(className);
	if (textContent)
		element.textContent = textContent;
	return element;
}

export function updateElt(elt, textContent)
{
	if (!elt)
		return ;
	elt.textContent = textContent;
}

export function importCSS(filePath)
{
	const head = getElt('head');
	const link = document.createElement('link');
	link.rel = 'stylesheet';
	link.href = filePath;
	head.appendChild(link);
}