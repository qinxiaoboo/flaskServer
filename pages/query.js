// Function to fetch data and populate the table
function fetchData() {
	fetch(`http://localhost:9000/envs/info?page=${currentPage}&pageSize=${pageSize}&sortBy=${sortBy}&sortOrder=${sortOrder}&search=${encodeURIComponent(searchQuery)}`)
	.then(response => response.json())
	.then(data => {
		console.log(data);
		data = data.data;
		const tableBody = document.querySelector('#data-table tbody');
		tableBody.innerHTML = ''; // Clear existing rows

		data.forEach(item => {
			const row = document.createElement('tr');
			row.innerHTML = `
				<td><input type="checkbox" class="row-checkbox" value="${item.id}" /></td>
				<td>${item.group}</td>
				<td>${item.env}</td>
				<td>${item.tw}</td>
				<td>${item.discord}</td>
				<td>${item.outlook}</td>
				<td>${item.ip}</td>
			`;
			tableBody.appendChild(row);
		});
		document.getElementById('page-info').textContent = `第 ${currentPage} 页`;
		document.getElementById('prev-page').disabled = (currentPage === 1);
		document.getElementById('next-page').disabled = (data.length < pageSize);
	}).catch(error => {
		console.error('Error fetching data:', error);
	});
}