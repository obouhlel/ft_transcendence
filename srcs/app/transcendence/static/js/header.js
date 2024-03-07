/*DROPDOWN FUNCTIONALITY*/
export function dropdown() {
	document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
		toggle.addEventListener('click', function(event) {
			event.preventDefault();
			const dropdownId = this.getAttribute('data-dropdown');
			toggleDropdown(event, dropdownId);
		});
	});
	
	function toggleDropdown(event, dropdownId) {
		const dropdown = document.getElementById(dropdownId);
		dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
		event.stopPropagation();
	}
	
	window.addEventListener('click', function() {
		hideDropdowns();
	});
	
	// Prevent clicks within the dropdown from closing it
	document.querySelectorAll('.dropdown-content, .dropdown-content-one').forEach(dropdown => {
		dropdown.addEventListener('click', function(event) {
			event.stopPropagation();
		});
	});
	
	// Hide all dropdowns
	function hideDropdowns() {
		document.querySelectorAll('.dropdown-content, .dropdown-content-one').forEach(dropdown => {
			dropdown.style.display = "none";
		});
	}
	
	const cross = document.getElementById('cross');
	if (cross) {
		cross.addEventListener('click', function(event) {
			event.stopPropagation();
			hideDropdown('userDropdown');
		});
	}
	
	// Function to hide a specific dropdown by its ID
	function hideDropdown(dropdownId) {
		const dropdown = document.getElementById(dropdownId);
		if (dropdown) {
			dropdown.style.display = "none";
		}
	}
}

export function responsiveNav(){
	let bar = document.getElementById("bar");
	let list = document.getElementById("list");

	bar.addEventListener("click", () => {
  		list.classList.toggle("show-list");
	});
}