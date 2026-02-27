page_no = 1;
all_page_param = ' 1=1 ';
layui.use(['form', 'layer', 'laydate'], function () {

    $ = layui.jquery;
    var form = layui.form,
        layer = layui.layer,
        laydate = layui.laydate;
    //执行一个laydate实例
    // laydate.render({
    //     elem: '#start' //指定元素
    // });
    //
    // //执行一个laydate实例
    // laydate.render({
    //     elem: '#end' //指定元素
    // });


//监听提交
    form.on('submit(edit)', function (data) {
        console.log(JSON.stringify(data.field));
        $.ajax({
            url: "/for/edit",
            data: data.field,
            method: "POST",
            success: function (obj) {
                layer.closeAll();
                layer.msg("修改成功！", {icon: 6})
                get_for_data(page_no)
            },
            error: function (xhr, type, errorThrown) {

            }
        });

        return false;
    });

});
get_for_data(page_no);
max_page = 0;

function get_for_data(no) {
    page_no = no;
    $.ajax({
        url: "/for/list",
        data: {"page_size": 10, "page_no": page_no, "param": all_page_param},
        method: "POST",
        success: function (obj) {
            page_data = obj.data;
            page_list = obj.page_list;
            max_page = obj.max_page;
            show_data(page_data, page_no, page_list)
        },
        error: function (xhr, type, errorThrown) {
        }
    })
}

function show_data(page_data, page_no, page_list) {
    list_data = '';
    for (var i = 0; i < page_data.length; i++) {
        item = page_data[i];
        console.log(item)
        list_data = list_data + '<tr>' +
            '<td>' + (i + 1) + '</td>' +
            '<td>' + item[1] + '</td>' +
            '<td>' + item[2] + '</td>' +
            '<td>' + item[3] + '</td>' +
            '<td>' + item[4] + '</td>' +
            '<td>' + item[5] + '</td>' +
            '<td>' + item[6] + '</td>' +
            '<td>' + item[7] + '</td>' +
            '          </tr>'
    }
    if (page_no == 1) {
        page_str = ''
    } else {
        page_str = '<span class="prev" onclick="get_for_data(' + (page_no - 1) + ')">&lt;&lt;</span>';
    }
    for (var i = 0; i < page_list.length; i++) {
        item = page_list[i];
        if (item == page_no) {
            page_str = page_str + '<span class="current">' + item + '</span>'
        } else {
            page_str = page_str + '<span class="num" onclick="get_for_data(' + item + ')">' + item + '</span>'
        }
    }
    if (page_no != max_page) {
        page_str = page_str + ' <span class="next" onclick="get_for_data(' + (page_no + 1) + ')">&gt;&gt;</span>'
    }

    $("#for_data").html(list_data);
    $("#page_list").html(page_str);

}

function x_new_edit(title, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, w, he) {
    if (w == null || w == '') {
        w = 600
    }
    if (he == null || he == '') {
        he = 550
    }
    $('#id').val(a);
    $('#time').val(b);
    $('#grainArea').val(c);
    $('#cottonArea').val(d);
    $('#oilArea').val(e);
    $('#sugraArea').val(f);
    $('#grainYield').val(g);
    $('#cottonYield').val(h);
    $('#oilYield').val(i);
    $('#sugraYield').val(j);
    $('#teaYield').val(k);
    $('#meatYield').val(l);
    $('#eggsYield').val(m);
    $('#milkYield').val(n);
    $('#aquaticYield').val(o);
    $('#woodYield').val(p);
    $('#landArea').val(q);
    $('#waterArea').val(r);
    layer.open({
        type: 1,
        area: [w + 'px', he + 'px'],
        fix: false, //不固定
        maxmin: true,
        shadeClose: true,
        shade: 0.4,
        title: title,
        content: $('#new-edit')
    });
}

/*删除*/
function member_del(obj, id) {
    layer.confirm('确认要删除吗？', function (index) {
        //发异步删除数据
        $(obj).parents("tr").remove();
        layer.msg('已删除!' + id, {icon: 1, time: 1000});
    });
}

/*查询*/
function get_search() {
    param = ' 1=1 ';
    time = $("#time").val();
    console.log(start)
    if (time != null) {
        param = param + " and time= '" + time + "'";
    }
    all_page_param = param;
    get_for_data(page_no)
}