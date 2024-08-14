window.addEventListener('DOMContentLoaded', (event) => {
    const token = '474b21d224a0f6'; // 替换为你的 ipinfo 访问令牌
    const url = `https://ipinfo.io/json?token=${token}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ip = data.ip;
            const city = data.city;
            const region = data.region;
            const country = data.country;
            const loc = data.loc; // 经纬度字符串，格式为 "lat,long"

            // 显示 IP 地址
            document.getElementById('result').innerHTML = `您的 IP 地址是: ${ip}`;

            // 显示位置信息
            document.getElementById('details').innerHTML = `
                城市: ${city}<br>
                省份: ${region}<br>
                国家: ${country}<br>
                经纬度: ${loc}<br>
                更多信息请访问 <a href="https://ipinfo.io/${ip}" target="_blank">ipinfo.io</a>
            `;
        })
        .catch(error => {
            document.getElementById('result').innerHTML = `查询失败: ${error}`;
            document.getElementById('details').innerHTML = '';
        });
});