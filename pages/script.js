  // 重置 GET请求
function handleRestOperation() {
	fetch('http://localhost:9000/chromes/reset')
	.then(data=>{
		alert('操作成功');
		console.log(data);
	}).catch(error => {
		console.error('Error fetching data:', error);
		alert('操作失败');
	})
}
 
 // 调试
function handleDebugOperation() {
	const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
	const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);

	if (selectedIds.length === 0) {
		alert('请选择要操作的行');
		return;
	}
	fetch('http://localhost:9000/envs/debug', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ ids: selectedIds }),
	}).then(response => response.json())
	.then(data=>{
		alert('批量操作成功');
		console.log(data);
	}).catch(error => {
		console.error('Error fetching data:', error);
		alert('批量操作失败');
	})
}

 // 初始化
function handleInitOperation() {
	const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
	const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);

	if (selectedIds.length === 0) {
		alert('请选择要操作的行');
		return;
	}
	fetch('http://localhost:9000/envs/init', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ ids: selectedIds }),
	}).then(response => response.json())
	.then(data=>{
		alert('批量操作成功');
		console.log(data);
	}).catch(error => {
		console.error('Error fetching data:', error);
		alert('批量操作失败');
	})
}