
/**
 * 通用表头操作
 */
function handleOperation(url) {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        url,
        { "ids": selectedIds },
        '重置操作成功',
        '重置操作失败'
    );
}
/**
 * 处理重置操作
 */
function handleRestOperation() {
    const resetType = document.getElementById("resetType").value;
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    if (resetType === "hard"){
        const confirmAction = window.confirm("您选择了硬重置操作，确定要继续吗？此操作无法撤销！");
        if (confirmAction) {
            sendPostRequest(
                'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/chromes/reset`,
                { "ids": selectedIds , "type": resetType},
                '重置操作成功',
                '重置操作失败'
            );
        } else {
            // 用户取消，不发送请求
            alert("操作已取消");
        }
    }else if (resetType === "soft"){
        sendPostRequest(
            'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/chromes/reset`,
            { "ids": selectedIds , "type": resetType},
            '重置操作成功',
            '重置操作失败'
        );
    }else {
        showAlert('请选择正确的重置操作类型');
    }

}
/**
 * 关闭浏览器操作
 */
function handleCloseOperation(){
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/chromes/close`,
        { "ids": selectedIds },
        '关闭操作成功',
        '关闭操作失败'
    );
}

/**
 * 删除浏览器操作
 */
function handleDeleteOperation(){
    const confirmAction = window.confirm("您选择了删除操作，确定要继续吗？此操作无法撤销！");
        if (confirmAction) {
            const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
            const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
            sendPostRequest(
                'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/chromes/delete`,
                { "ids": selectedIds },
                '删除操作成功',
                '删除操作失败'
            );
            fetchData()
        } else {
            // 用户取消，不发送请求
            alert("操作已取消");
        }
}

/**
 * 处理调试操作
 */
function handleDebugOperation() {
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    sendPostRequest(
        'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/envs/debug`,
        { "ids": selectedIds },
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
        'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/envs/init`,
        { "ids": selectedIds },
        '初始化操作成功',
        '初始化操作失败'
    );
}

// 提交表单并显示进度
function handleUploadFile(e) {
    e.preventDefault(); // 阻止表单默认提交
    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    // 获取表单数据
    const formData = new FormData(this);  // 获取表单数据
    const file = formData.get('file');    // 获取文件
    formData.append('ids', JSON.stringify(selectedIds));
    // 获取进度条和状态元素
    const progressBar = document.getElementById('progressBar');
    const status = document.getElementById('status');

    // 显示进度条
    progressBar.style.display = 'block';

    // 创建 XMLHttpRequest 实例
    const xhr = new XMLHttpRequest();

    // 设置上传进度监听
    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100;
            progressBar.value = percent;
        }
    };

    // 设置上传完成后的回调
    xhr.onload = function () {
        if (xhr.status === 200) {
            status.textContent = '文件上传成功！';
        } else {
            status.textContent = '上传失败，请重试！';
        }
        progressBar.style.display = 'none';  // 隐藏进度条
    };

    // 设置上传失败的回调
    xhr.onerror = function () {
        status.textContent = '上传失败，请检查网络连接！';
        progressBar.style.display = 'none';  // 隐藏进度条
    };

    // 启动文件上传
    xhr.open('POST', 'http://' + server_address + ':' + server_port + `/${localStorage.getItem("groups")}/envs/upload`, true );
    xhr.send(formData);
    fetchData()
}
/**
 * 发送 POST 请求的通用函数
 * @param {string} url 请求的 URL
 * @param {Array<string>} body 要发送的 body
 * @param {string} successMessage 操作成功时的提示消息
 * @param {string} errorMessage 操作失败时的提示消息
 */
function sendPostRequest(url, body, successMessage, errorMessage) {
    if (body.ids.length === 0) {
        showAlert('请选择要操作的行');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(body),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.code===0){
            showAlert(data.msg);
        }else {
            showAlert(data.error)
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        showAlert(errorMessage);
    });
}