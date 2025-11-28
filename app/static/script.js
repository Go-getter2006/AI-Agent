// C Tutor 前端 JavaScript
console.log('C Tutor 前端脚本加载完成');

// 基本的 WebSocket 连接测试
function testWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    console.log('尝试连接到:', wsUrl);

    const ws = new WebSocket(wsUrl);

    ws.onopen = function() {
        console.log('✅ WebSocket 连接成功');
        // 发送测试消息
        ws.send(JSON.stringify({
            type: 'user_message',
            content: '测试连接',
            code_context: {}
        }));
    };

    ws.onmessage = function(event) {
        console.log('收到消息:', event.data);
        try {
            const data = JSON.parse(event.data);
            alert('WebSocket 测试成功！服务器回应: ' + data.content);
        } catch (e) {
            console.error('解析消息失败:', e);
        }
        ws.close();
    };

    ws.onerror = function(error) {
        console.error('WebSocket 连接错误:', error);
        alert('WebSocket 连接失败，请检查后端服务是否运行');
    };

    ws.onclose = function() {
        console.log('WebSocket 连接关闭');
    };
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('C Tutor 页面加载完成');

    // 添加测试按钮
    const testLinks = document.querySelector('.test-links');
    const testBtn = document.createElement('a');
    testBtn.href = '#';
    testBtn.className = 'btn';
    testBtn.textContent = '测试WebSocket';
    testBtn.onclick = function(e) {
        e.preventDefault();
        testWebSocket();
    };
    testLinks.appendChild(testBtn);
});
