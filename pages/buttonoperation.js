/**
 * 处理重置操作
 */
function handleRestOperation() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://localhost:9000/chromes/reset',
        selectedIds,
        '重置操作成功',
        '重置操作失败'
    );
}

/**
 * 处理调试操作
 */
function handleDebugOperation() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://localhost:9000/envs/debug',
        selectedIds,
        '调试操作成功',
        '调试操作失败'
    );
}

/**
 * 处理初始化操作
 */
function handleInitOperation() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://localhost:9000/envs/init',
        selectedIds,
        '初始化操作成功',
        '初始化操作失败'
    );
}

/**
 * 发送 POST 请求的通用函数
 * @param {string} url 请求的 URL
 * @param {Array<string>} ids 要发送的 ID 列表
 * @param {string} successMessage 操作成功时的提示消息
 * @param {string} errorMessage 操作失败时的提示消息
 */
function sendPostRequest(url, ids, successMessage, errorMessage) {
    if (ids.length === 0) {
        alert('请选择要操作的行');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ids: ids }),
    })
    .then(response => response.json())
    .then(data => {
        alert(successMessage);
        console.log(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert(errorMessage);
    });
}