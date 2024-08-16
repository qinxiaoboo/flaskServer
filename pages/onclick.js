function changePage(direction) {
	currentPage += direction;
	fetchData();
}

function sortData(field) {
	if (sortBy === field) {
		sortOrder = (sortOrder === 'asc') ? 'desc' : 'asc';
	} else {
		sortBy = field;
		sortOrder = 'asc';
	}
	fetchData();
}

