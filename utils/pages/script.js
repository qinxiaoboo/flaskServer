window.addEventListener('DOMContentLoaded', (event) => {
    // IPINFO密码统一为：123qweasd ，，一个token一个月5万次请求，不够请注册账号增加token，注册地址：https://ipinfo.io/signup
    // Q-4-1
    const tokens = ['474b21d224a0f6', '49c2ab4ff7a1cf', 'a206ea7361154a', '3c7e33c84deaef', '5751b568430384'
    , '92190d75d1c110', 'bacf74eb433ba7', '207da94d85058c']; // 替换为你的 token 列表
    // 随机选择一个 token
    const randomToken = tokens[Math.floor(Math.random() * tokens.length)];
    const url = `https://ipinfo.io/json?token=${randomToken}`;

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
function getBrowserFingerprint() {
            // Basic information
            const userAgent = navigator.userAgent;
            const platform = navigator.platform;
            const language = navigator.language;
            const screenWidth = screen.width;
            const screenHeight = screen.height;
            const colorDepth = screen.colorDepth;
            const timezoneOffset = new Date().getTimezoneOffset();
            const deviceMemory = navigator.deviceMemory || 'unknown'; // Device memory might not be available
            const hardwareConcurrency = navigator.hardwareConcurrency || 'unknown'; // Number of logical processors

            // Advanced information (may need more complex methods)
            const screenOrientation = screen.orientation ? screen.orientation.type : 'unknown';
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            const pixelRatio = window.devicePixelRatio;
            const browserLanguage = navigator.languages ? navigator.languages.join(', ') : language;

            return {
                userAgent,
                platform,
                language,
                screenWidth,
                screenHeight,
                colorDepth,
                timezoneOffset,
                deviceMemory,
                hardwareConcurrency,
                screenOrientation,
                viewportWidth,
                viewportHeight,
                pixelRatio,
                browserLanguage
            };
        }

        function displayFingerprint() {
            const fingerprint = getBrowserFingerprint();
            document.getElementById('user-agent').textContent = `用户代理: ${fingerprint.userAgent}`;
            document.getElementById('platform').textContent = `平台: ${fingerprint.platform}`;
            document.getElementById('language').textContent = `语言: ${fingerprint.browserLanguage}`;
            document.getElementById('screen-size').textContent = `屏幕尺寸: ${fingerprint.screenWidth}x${fingerprint.screenHeight}`;
            document.getElementById('color-depth').textContent = `色彩深度: ${fingerprint.colorDepth} 位`;
            document.getElementById('timezone').textContent = `时区偏移: ${fingerprint.timezoneOffset} 分钟`;
            document.getElementById('device-memory').textContent = `设备内存: ${fingerprint.deviceMemory} GB`;
            document.getElementById('hardware-concurrency').textContent = `硬件并发: ${fingerprint.hardwareConcurrency} 线程`;
            document.getElementById('screen-orientation').textContent = `屏幕方向: ${fingerprint.screenOrientation}`;
            document.getElementById('viewport-size').textContent = `视口尺寸: ${fingerprint.viewportWidth}x${fingerprint.viewportHeight}`;
            document.getElementById('pixel-ratio').textContent = `设备像素比: ${fingerprint.pixelRatio}`;
        }

        window.onload = displayFingerprint;
(async () => {
    // Initialize FingerprintJS
    const fp = await FingerprintJS.load();

    // Get the visitor identifier
    const result = await fp.get();
    const fingerprint = result.visitorId;

    // Display the fingerprint
    document.getElementById('fingerprint').textContent = `指纹: ${fingerprint}`;
})();