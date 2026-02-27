page_no = 1;
all_page_param = ' 1=1 ';
layui.use(['form', 'layer', 'laydate'], function () {

    $ = layui.jquery;
    var layer = layui.layer;
    $("#a1").val(1);
    $("#a2").val(1);
    $("#a3").val(14);
    $("#a4").val(21);
    $("#a5").val(0.01);
    //预测数据
    window.predict = function () {
        let a1 = $("#a1").val();
        let a2 = $("#a2").val();
        let a3 = $("#a3").val();
        let a4 = $("#a4").val();
        let a5 = $("#a5").val();
        if (a1 < 0 || a1 > 1) {
            return layer.msg("接触率在0-1之间！")
        }
        if (a2 < 0 || a2 > 1) {
            return layer.msg("传染率在0-1之间！")
        }
        if (a3 < 0) {
            return layer.msg("隔离期需大于0！")
        }
        if (a4 < 0) {
            return layer.msg("潜伏期需大于0！")
        }
        if (a5 < 0 || a5 > 1) {
            return layer.msg("突发事件率在0-1之间！")
        }

        let index = layer.load();
        $.ajax({
            url: "/cov/predict",
            method: "POST",
            data: {"a1": a1, "a2": a2, "a3": a3, "a4": a4, "a5": a5},
            success: function (obj) {
                layer.close(index);
                var add = echarts.init(document.getElementById("add"));
                var add_option = {
                    color: ['#c89b1c'],
                    title: {
                        text: '未来14日每日新增预测',
                        textStyle: {
                            color: 'black'
                        },
                        left: 'left'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    xAxis: {
                        type: 'category',
                        data: obj.X
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: obj.add,
                            type: 'line'
                        }
                    ]
                };
                add.setOption(add_option);
                layer.msg("预测成功！", {icon: 6})
            },
            error: function (xhr, type, errorThrown) {
            }
        });
    }
});

