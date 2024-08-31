server_address="localhost"
server_port = "9000"
// 加载公共组件
async function loadComponent(id, url) {
    const response = await fetch(url);
    const text = await response.text();
    ele = document.getElementById(id)
    if (ele){
        ele.innerHTML = text;
    }
}

// 加载头部和底部
loadComponent('header', '../views/header.html');