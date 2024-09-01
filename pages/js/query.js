function getAccountColor(status){
	return status === 0 ? 'gray' :
		status === 1 ? 'red' :
		status === 2 ? 'green' : 'black';
}

// Function to fetch data and populate the table
function fetchData({page=0,size=0,search=undefined,label=""}={}) {
	fetch(`http://${server_address}:${server_port}/envs/info?page=${page===0?currentPage:page}&pageSize=${size===0?pageSize:size}&sortBy=${sortBy}&sortOrder=${sortOrder}&search=${encodeURIComponent(search===undefined?searchQuery:search)}&label=${encodeURIComponent(label)}`,
		{headers: {
				'Content-Type': 'application/json;charset=UTF-8',
				"token": localStorage.getItem("token")
				}
		})
	.then(response => response.json())
	.then(res => {
		if (res.code===0){
			data = res.data;
			const tableBody = document.querySelector('#data-table tbody');
			tableBody.innerHTML = ''; // Clear existing rows

			data.forEach(item => {
				const row = document.createElement('tr');
				row.innerHTML = `
					<td><input type="checkbox" class="row-checkbox" value="${item.id}" /></td>
					<td>${item.group}</td>
					<td>
						<span
							style="color: ${item.isOpen === 0 ? 'black' : item.isOpen === 1 ?  'green' : 'gray'}"
							title="${item.isOpen===0?'未运行':'在运行'}"
						>
						${item.env}
						</span></td>
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
					<td>
						<span 
							style="color: ${getAccountColor(item.ip_status)};" 
						>
							${item.ip}
						</span>
					</td>
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
		}else {
			if (res.error==="noLogin"){
				alert("请登录")
				window.location.assign('login.html');
			}else {
				alert(res.error)
			}
		}

	}).catch(error => {
		console.error('Error fetching data:', error);
	});
}

function fetchDataByLabel(){
	fetchData({page:1,size:100000,search:"",label:searchQuery})
}
function updateStatus(elementId, value) {
	const element = document.getElementById(elementId);
	if (value > 85) {
		element.textContent = `${elementId.replace('-', ' ').toUpperCase()}: ${value}%`;
		element.classList.add('warning');
		element.classList.remove('normal');
	} else {
		element.textContent = `${elementId.replace('-', ' ').toUpperCase()}: ${value}%`;
		element.classList.add('normal');
		element.classList.remove('warning');
	}
}

async function fetchSystemInfo() {
	request.get(`/${localStorage.getItem("groups")}/systeminfo`)
	.then(response => response.json())
	.then(res => {
		if (res.code===0){
			data = res.data
		 	updateStatus('cpu-usage', data.cpu_usage);
			updateStatus('memory-usage', data.memory_usage);
			updateStatus('disk-usage', data.disk_usage);
		}else {
			if (res.error==="noLogin"){
				alert("请登录")
				window.location.assign('login.html');
			}else{
				alert(data.error)
			}
		}
	})
}