function openmodal(modal_id) {
    $("#" + modal_id).modal();
}

function delPackage(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');
    if (packages_selected.length > 0) {
        postsubmit('/package_action?action=del', JSON.stringify(packages_selected), function (response) {
            response_dialog(response, function () {
                bootbox.alert("订单成功删除!", function () {
                    loadSubPage("packages");
                });
            })
        });
    }
}

function genpdf(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');
    if (packages_selected.length > 0) {
        run_waitMe($("#packagelist"), '提交中，请等待。。。。');
        postsubmit('/package_action?action=pdf', JSON.stringify(packages_selected), function (response) {
            $("#packagelist").waitMe('hide');
            if (response.status == 200) {
                download('面单.pdf', "data:application/pdf;base64,", response.msg)
            } else {
                alert(response.msg)
            }
        });
    }
}

function genexecel(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');
    if (packages_selected.length > 0) {
        run_waitMe($("#ordertorecievepage"), '提交中，请等待。。。。');
        postsubmit('/ordertorecieve?action=excel', JSON.stringify(packages_selected), function (response) {
            $("#ordertorecievepage").waitMe('hide');
            if (response.status == 200) {
                download('订单详情.xlsx', "data:application/ms-excel;base64,", response.msg)
            } else {
                alert(response.msg)
            }
        });
    }
}

function cancelpackages(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');
    if (packages_selected.length > 0) {

        for (var i = 0; i < packages_selected.length; i++) {
            var p = packages_selected[i];
            if (p['status'] != '已支付') {
                bootbox.alert('包裹单：' + p['order_no'] + '状态为' + p['status'] + '不可取消，只可取消已支付包裹，请重新选择！')
                return;
            }
        }
        postsubmit('/ordertorecieve?action=cancel', JSON.stringify(packages_selected), function (response) {
            if (response.status == 200) {
                bootbox.alert('包裹取消成功！', function () {
                    loadSubPage("ordertorecieve");
                })
            } else {
                bootbox.alert('包裹取消失败：' + response.msg);
            }
        });
    }
}

function PackageDetailFormatter(value, row, index) {
    return "<a href='#' onclick='checkPackage(" + row.id + ")' style='color: blue;'>" + value + "</a>";
}

function PackageExpressDetailFormatter(value, row, index) {
    if (row.logistic_product === 'shunfeng') {
        return "<p>" + row.logistic_product + "</p>" + "<p> 月结卡：" + row.express_extra.sf_month_card + "</p>"+ "<p> 目的地代码：" + row.express_extra.destination_code + "</p>";
    } else {
        return "<p>" + row.logistic_product + "</p>";

    }

}


function checkPackage(pid) {
    loadSubPage("package_detail?pid=" + pid);
}

function editOrder(oid) {
    loadSubPage("onlineorder?pid=" + oid);
}

function sortPackage(pagename) {

    var search_date_start = $('#search-date-start').val();
    var search_date_end = $('#search-date-end').val();

    if (search_date_start.length > 0 && search_date_end.length > 0) {
        if (moment(search_date_start).isAfter(search_date_end)) {
            bootbox.alert("起始时间不能大于结束时间，请重新选择日期");
            return;
        }
    }

    console.log(pagename + "?search_date_start=" + search_date_start + "&search_date_end=" + search_date_end);

    loadSubPage(pagename + "?search_date_start=" + search_date_start + "&search_date_end=" + search_date_end);
}

function startcomplain(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');
    if (packages_selected.length > 0) {
        var order_nos = "";
        for (var i = 0; i < packages_selected.length; i++) {
            order_nos += packages_selected[i]['order_no'] + ','
        }
        loadSubPage('complain?order_nos=' + order_nos);
    } else {
        loadSubPage('complain');
    }
}

function startclaim(table_id) {
    let packages_selected = $("#" + table_id).bootstrapTable('getAllSelections');

    if (packages_selected.length > 0) {
        var order_nos = "";
        for (var i = 0; i < packages_selected.length; i++) {
            order_nos += packages_selected[i]['order_no'] + ','
        }
        loadSubPage('claim?order_nos=' + order_nos);
    } else {
        loadSubPage('claim');
    }
}


function OriginalFileFormatter(value, row, index) {
    if (row.orginal_file) {
        return "<a href='" + row.orginal_file + "' style='color: blue;'>" + value + "</a>";
    } else {
        return value;
    }
}

function ResultFileFormatter(value, row, index) {
    if (row.result_file) {
        return "<a href='" + row.result_file + "' style='color: blue;'>" + value + "</a>";
    } else {
        return value;
    }
}

function searchoders() {
    var starttime = moment($('#time-start').val());
    var endtime = moment($('#time-end').val());
    if (starttime.isAfter(endtime)) {
        bootbox.alert("结束时间必须大于起始时间");
        return;
    }

    var search_array_name = $('#search_array_name').val();
    var search_array = $('#search_array').val().trim();
    var pakcage_status = $('#pakcage_status').val();

    if (!starttime.isValid() && !endtime.isValid() && search_array.length == 0 && pakcage_status == "-1") {
        bootbox.alert("必须填写至少一个筛选条件");
        return;
    }

    $("#ems-single-btn-to-search").html('查询中，请等待。。。。。');
    $('#ems-single-btn-to-search').prop("disabled", true);

    json_content = {
        'starttime': starttime.isValid() ? starttime.format("YYYY-MM-DD") : "2000-10-10",
        'endtime': endtime.isValid() ? endtime.format("YYYY-MM-DD") : "2100-10-10",
        'search_array_name': search_array_name,
        'search_array': search_array.length > 0 ? search_array.split(" ") : [],
        'pakcage_status': pakcage_status
    };

    postsubmit('/orderfilter', JSON.stringify(json_content), function (response) {
        if (response.status == 200) {
            if (response.msg.rows.length > 0) {
                bootbox.alert('共找到' + response.msg.rows.length + '记录');
                $('#to-recieve-list-sorted-table').bootstrapTable({data: ""});
                $('#to-recieve-list-sorted-table').bootstrapTable('load', response.msg.rows);
            } else {
                bootbox.alert('为找到符合条件的包裹单，请调整条件后重新查询');
            }

            //$('#to-recieve-list-table').bootstrapTable();
        } else {
            bootbox.alert('Error：' + response.msg);
        }

        $('#ems-single-btn-to-search').prop("disabled", false);
        $("#ems-single-btn-to-search").html('查询');
    });

}