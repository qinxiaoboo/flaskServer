// 生成弹框 HTML
function createAlertBox() {
  var existingAlert = document.getElementById('customAlert');
  if (!existingAlert) {
    var alertBox = document.createElement('div');
    alertBox.id = 'customAlert';
    alertBox.style.display = 'none'; // 初始状态隐藏
    alertBox.style.position = 'fixed';
    alertBox.style.top = '10%'; // 距离顶部10%
    alertBox.style.left = '50%'; // 水平居中
    alertBox.style.transform = 'translateX(-50%)'; // 水平偏移50%
    alertBox.style.padding = '20px';
    alertBox.style.background = 'linear-gradient(135deg, #ff7e5f, #feb47b)'; // 渐变背景
    alertBox.style.color = '#fff';
    alertBox.style.width = '300px'; // 设置宽度
    alertBox.style.height = '10px'; // 设置高度
    alertBox.style.borderRadius = '10px'; // 圆角边框
    alertBox.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)'; // 阴影
    alertBox.style.zIndex = '10000'; // 确保弹框在最上层
    alertBox.style.fontFamily = 'Arial, sans-serif'; // 字体
    alertBox.style.fontSize = '16px'; // 字体大小
    alertBox.style.textAlign = 'center'; // 居中文本
    alertBox.style.border = '1px solid #fff'; // 边框
    alertBox.style.opacity = '0'; // 初始透明度为0
    alertBox.style.transition = 'opacity 0.5s ease-in-out'; // 过渡动画
    document.body.appendChild(alertBox);
  }
}

// 显示弹框并设置内容
function showAlert(message, color = '#4CAF50') {
  createAlertBox(); // 确保弹框 HTML 已存在
  var alertBox = document.getElementById('customAlert');
  alertBox.textContent = message; // 设置弹框的文本内容
  alertBox.style.background = color; // 设置背景颜色
  alertBox.style.display = 'block'; // 显示弹框
  alertBox.style.opacity = '1'; // 使弹框可见
  setTimeout(function() {
    alertBox.style.opacity = '0'; // 过渡消失
    setTimeout(function() {
      alertBox.style.display = 'none'; // 5秒后隐藏弹框
    }, 500); // 等待过渡动画完成
  }, 5000); // 5000毫秒 = 5秒
}