//定义画布
var ocrDemo = {
    CANVAS_WIDTH: 200,
    TRANSLATED_WIDTH: 20,
    PIXEL_WIDTH: 10, // TRANSLATED_WIDTH = CANVAS_WIDTH/PIXEL_WIDTH
    BATCH_SIZE: 1,

    PORT: '9000',
    HOST: 'http://localhost',

    BLACK: '#000000',
    BLUE: '0000FF',

    //客户端训练数据集
    trainArray: [],
    trainingRequestCount: 0,

    onLoadFunction: function () {
        this.resetCanvas();
    },

    resetCanvas: function () {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');

        this.data = [];
        ctx.fillStyle = this.BLACK;
        ctx.fillRect(0, 0, this.CANVAS_WIDTH, this.CANVAS_WIDTH);
        var matrixSize = 400;
        while (matrixSize--) this.data.push(0);
        this.drawGrid(ctx);

        // 绑定事件操作
        canvas.onmousemove = function (e) { this.onMouseMove(e, ctx, canvas) }.bind(this);
        canvas.onmousedown = function (e) { this.onMouseDown(e, ctx, canvas) }.bind(this);
        canvas.onmouseup = function (e) { this.onMouseUp(e, ctx) }.bind(this);
    },

    //在画布上加上网格辅助输入和查看
    drawGrid: function (ctx) {
        for (var x = this.PIXEL_WIDTH, y = this.PIXEL_WIDTH;
            x < this.CANVAS_WIDTH; x += this.PIXEL_WIDTH,
            y += this.PIXEL_WIDTH) {
            ctx.strokeStyle = this.BLUE; // 笔触的颜色、渐变或模式
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, this.CANVAS_WIDTH);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(this.CANVAS_WIDTH, y);
            ctx.stroke(); //stroke() 方法会实际地绘制出通过 moveTo() 和 lineTo() 方法定义的路径
        }
    },

    onMouseMove: function (e, ctx, canvas) {
        if (!canvas.isDrawing) {
            return;
        }
        this.fillSquare(ctx, e.clientX - canvas.offsetLeft,
            e.clientY - canvas.offsetTop);
    },

    onMouseDown: function (e, ctx, canvas) {
        canvas.isDrawing = true;
        this.fillSquare(ctx, e.clientX - canvas.offsetLeft,
            e.clientY - canvas.offsetTop);
    },

    onMouseUp: function (e) {
        canvas.isDrawing = false;
    },

    fillSquare: function (ctx, x, y) {
        var xPixel = Math.floor(x / this.PIXEL_WIDTH);
        var yPixel = Math.floor(y / this.PIXEL_WIDTH);
        this.data[((xPixel - 1) * this.TRANSLATED_WIDTH + yPixel) - 1] = 1;

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(xPixel * this.PIXEL_WIDTH, yPixel * this.PIXEL_WIDTH,
            this.PIXEL_WIDTH, this.PIXEL_WIDTH);
    },

    train: function () {
        var digitVal = document.getElementById('digit').value;
        //没有输入标签或者没有手写输入就报错
        if (!digitVal || this.data.indexOf(1) < 0) { 
            alert("Please type and draw a digit value in order to train the network");
            return;
        }
        //将训练数据加到客户端训练集中
        this.trainArray.push({ "y0": this.data, "label": parseInt(digitVal) });
        this.trainingRequestCount++;

        //训练数据达到指定的量是就发送给服务器端
        //设置BATCH_SIZE是为了防止服务器在短时间内处理过多请求而降低服务器性能
        if (this.trainingRequestCount == this.BATCH_SIZE) { 
            alert("Sending training data to server...");
            var json = {
                trainArray: this.trainArray,
                train: true
            };

            this.sendData(json);
            //清空客户端训练集
            this.trainingRequestCount = 0;
            this.trainArray = [];
        }
    },

    //客户端点击测试键
    test: function () {
        if (this.data.indexOf(1) < 0) { 
            alert('Please draw a digit in order to test the network.');
            return;
        }
        var json = {
            image: this.data,
            predict: true
        };
        this.sendData(json);
    },

    // 处理服务器响应
    receiveResponse: function (xmlHttp) { 
        if (xmlHttp.status != 200) {
            alert('Server return status ' + xmlHttp.status);
            return;
        }        
        var responseJSON = JSON.parse(xmlHttp.responseText);
        if (xmlHttp.responseText && responseJSON.type == "test") {
            alert("The neural network predicts you wrote a \'" +
                responseJSON.result + '\'');
        }
    },

    onError: function (e) {
        alert("Error occurred while connecting to server: " + e.target.statusText);
    },

    sendData: function (json) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open('POST', this.HOST + ':' + this.PORT, false);
        xmlHttp.onload = function () {
            this.receiveResponse(xmlHttp);
        }.bind(this);
        xmlHttp.onerror = function () {
            this.onError(xmlHttp);
        }.bind(this);
        var msg = JSON.stringify(json);
        xmlHttp.setRequestHeader('Content-length', msg.length);
        xmlHttp.setRequestHeader('Connection', 'close');
        xmlHttp.send(msg);
    }
}

