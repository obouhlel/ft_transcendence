import { main } from './app.js';

export function getElt(selector)
{
	if (!selector)
		return null;
	else if (document.querySelector(selector) !== null)
		return document.querySelector(selector);
	else if (document.getElementById(selector) !== null)
		return document.getElementById(selector);
	else if (document.getElementsByClassName(selector) !== null)
		return document.getElementsByClassName(selector);
	else if (document.getElementsByTagName(selector) !== null)
		return document.getElementsByTagName(selector);
	else
		return null;
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

export function resizeMain()
{
	const footer = getElt('footer');
	const footerRect = footer.getBoundingClientRect();
	const header = getElt('header');
	const headerRect = header.getBoundingClientRect();
	
	main.style.marginTop = `${headerRect.bottom}px`;
}