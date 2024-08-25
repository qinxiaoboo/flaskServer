function getAccountColor(status){
	return status === 0 ? 'gray' :
		status === 1 ? 'red' :
		status === 2 ? 'green' : 'black';
}

// Function to fetch data and populate the table
function fetchData({page=0,size=0,search=undefined,label=""}={}) {
	fetch(`http://localhost:9000/envs/info?page=${page===0?currentPage:page}&pageSize=${size===0?pageSize:size}&sortBy=${sortBy}&sortOrder=${sortOrder}&search=${encodeURIComponent(search===undefined?searchQuery:search)}&label=${encodeURIComponent(label)}`,
		{headers: {
				'Content-Type': 'application/json;charset=UTF-8'
				}
		})
	.then(response => response.json())
	.then(res => {
		data = res.data;
		const tableBody = document.querySelector('#data-table tbody');
		tableBody.innerHTML = ''; // Clear existing rows

		data.forEach(item => {
			const row = document.createElement('tr');
			row.innerHTML = `
				<td><input type="checkbox" class="row-checkbox" value="${item.id}" /></td>
				<td>${item.group}</td>
				<td>${item.env}</td>
				<td>
					<span 
						style="color: ${getAccountColor(item.tw_status)};" 
						title="${item.tw_error || ''}"
					>
						${item.tw}
					</span>
				</td>
				<td>
					<span 
						style="color: ${getAccountColor(item.discord_status)};" 
						title="${item.discord_error || ''}"
					>
						${item.discord}
					</span>
				</td>
				<td>
					<span 
						style="color: ${getAccountColor(item.outlook_status)};" 
						title="${item.outlook_error || ''}"
					>
						${item.outlook}
					</span>
				</td>
				<td>${item.ip}</td>
				<td>${item.status}</td>
				<td>${item.label}</td>
			`;
			tableBody.appendChild(row);
		});
		document.getElementById('page-info').textContent = `第 ${currentPage} 页`;
		document.getElementById('prev-page').disabled = (currentPage === 1);
		document.getElementById('next-page').disabled = (data.length < pageSize);
		 // 更新数据总数
        document.getElementById('totalCount').innerText = `Total Count: ${res.total}`;
	}).catch(error => {
		console.error('Error fetching data:', error);
	});
}

function fetchDataByLabel(){
	fetchData({page:1,size:100000,search:"",label:searchQuery})
}