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

/**
 * 处置设置标签操作
 */
function restsLabel() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://' + server_address + ':' + server_port + '/envs/set/label',
        { "ids": selectedIds, "label": searchQuery },
        '设置标签操作成功',
        '设置标签操作失败'
    );
	fetchData({search:""})
}
/**
 * 处置设置标签操作
 */
function addLabel() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://' + server_address + ':' + server_port + '/envs/add/label',
        { "ids": selectedIds, "label": searchQuery },
        '追加标签操作成功',
        '追加标签操作失败'
    );
	fetchData({search:""})
}
/**
 * 重置全局变量
 */
function resetLocal(){
        lastChecked = null;
        currentPage = 1;
        pageSize = 12; // 每页显示的条目数
		sortBy = 'env';
        sortOrder = 'asc';
        document.getElementById('search').value=""
		searchQuery=""
		fetchData()
}