function moveItemToPosition(array, item, position) {
    // 查找要移动的对象的索引
    const index = array.indexOf(item);

    // 确保对象存在于列表中
    if (index > -1 && position >= 0 && position < array.length) {
        // 移除对象
        array.splice(index, 1);
        // 将对象插入到目标位置
        array.splice(position, 0, item);
    }
}
function removeItem(array, item){
    // 查找要移动的对象的索引
    const index = array.indexOf(item);

    // 确保对象存在于列表中
    if (index > -1) {
        // 移除对象
        array.splice(index, 1);
    }
}

// 判断是否为有效日期
function isValidDate(value) {
    const date = new Date(value);
    return !isNaN(date.getTime());
}

// 格式化日期
function formatDate(date) {
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}