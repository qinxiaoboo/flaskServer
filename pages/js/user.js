let users = [];
let currentIndex = -1; // 当前选中的用户索引
function renderUserTable() {
    const tbody = document.querySelector('#user-table tbody');
    tbody.innerHTML = '';
    fetch(`http://${server_address}:${server_port}/user/info`)
	.then(response => response.json())
    	.then(res => {
            if (res.code===0){
                console.log(res)
                users = []
                res.data.forEach((user, index) => {
                users.push(user)
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.name}</td>
                    <td>${user.groups}</td>
                    <td>
                        <button class="edit" onclick="editUser(${index})">编辑</button>
                        <button class="delete" onclick="deleteUser(${index})">删除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            }
        })
}

async function addUser() {
    const username = document.getElementById('username').value;
    const groups = document.getElementById('groups').value;
    const password = document.getElementById('password').value;

    if (username && groups && password ) {
        fetch(`http://${server_address}:${server_port}/user/add`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "token": localStorage.getItem("token")
            },
            body: JSON.stringify({"username":await encryptData(username),"password":await encryptData(password),"groups":await encryptData(groups)})
        })
        .then(response => response.json())
            .then(data=>{
                if (data.code === 0){
                    showAlert("操作成功")
                }else {
                    if (data.error === "noLogin"){
                        showAlert("请登录")
                        window.location.assign('login.html');
                    }else {
                        showAlert(data.error)
                    }
                }
            })
        renderUserTable();
        clearForm();
    } else {
        showAlert('请填写所有字段');
    }
}

function deleteUser(index) {
    console.log(users)
    renderUserTable();
}

function editUser(index) {
    currentIndex = index;
    const user = users[index];
    document.getElementById('username').value = user.name;
    document.getElementById('groups').value = user.groups;
    document.getElementById('password').value = user.password;
}

function clearForm() {
    document.getElementById('username').value = '';
    document.getElementById('groups').value = '';
    document.getElementById('password').value = '';
}

function updateUser() {
    if (currentIndex !== -1) {
        addUser(); // 调用 addUser 实现更新功能
    } else {
        showAlert('请选择要编辑的用户');
    }

}

