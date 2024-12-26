// 监听输入框事件
document.getElementById('search').addEventListener('input', (event) => {
		// 获取输入框的值, 并赋值给全局变量
		searchQuery = event.target.value;
		label = "";
})


// 监听表头点击事件
document.getElementById('reset-chrome-setting').addEventListener('click', handleRestOperation);
document.getElementById('debug-action-button').addEventListener('click', handleDebugOperation);
document.getElementById('init-action-button').addEventListener('click', handleInitOperation);
document.getElementById('close-chrome-button').addEventListener('click', handleCloseOperation);
document.getElementById('delete-action-button').addEventListener('click', handleDeleteOperation);

 // 监听文件上传
document.getElementById('uploadForm').addEventListener('submit', handleUploadFile);

// 监听选择事件
document.getElementById('select-all').addEventListener('change', (event) => {
	const checked = event.target.checked;
	document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = checked);
});
// // 监听查询提交事件
// document.getElementById('filter-form').addEventListener('submit', function(event) {
// 	event.preventDefault();
// 	searchQuery = document.getElementById('search').value;
// 	console.log(searchQuery)
// 	fetchData();
// });


// 监听多选事件
document.querySelector('#data-table').addEventListener('click', function(event) {
	if (event.target.type === 'checkbox' && event.target.classList.contains('row-checkbox')) {
		const currentCheckbox = event.target;
		if (event.shiftKey && lastChecked) {
			const checkboxes = Array.from(document.querySelectorAll('.row-checkbox'));
			const start = checkboxes.indexOf(lastChecked);
			const end = checkboxes.indexOf(currentCheckbox);

			if (start > end) {
				[start, end] = [end, start];
			}

			for (let i = start; i <= end; i++) {
				checkboxes[i].checked = lastChecked.checked;
			}
		}

		lastChecked = currentCheckbox;
	}
});