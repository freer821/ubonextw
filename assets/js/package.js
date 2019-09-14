var goods_selected = [];

function updateTableContent(g, num) {
    return '<td>' + g.cn_name + '</td>' + '<td>' + g.category + '</td>'  + '<td >' + g.brutto_weight+ '</td>' + '<td>' + g.ean_code + '</td>' + '<td>' + g.sale_price + '</td>' + '<td class="ems-single-table-middle">' + num + '</td>';
}

function createTableContent(id, g, num) {
    return '<tr id="' + id + '"><td>' + g.cn_name + '</td>'  + '<td>' + g.category + '</td>' + '<td>' + g.brutto_weight + '</td>' + '<td>' + g.ean_code + '</td>' + '<td>' + g.sale_price + '</td>' + '<td class="ems-single-table-middle">' + num + '</td></tr>';
}

function updateGoodSelected(goods_id, good, num) {
    var tr_id = "selected_goods" + goods_id;
    if (num > 0) {
        if ($("#" + tr_id).length) {
            $("#" + tr_id).html(updateTableContent(good, num));
            goods_selected.forEach(function (g) {
                if (g.ean_code == good.ean_code) {
                    g.num = num;
                }
            });
        } else {
            $("#goods_selected").append(createTableContent(tr_id, good, num));
            good.num = num;
            goods_selected.push(good);
        }
    } else {
        $("#" + tr_id).remove();
        for (var i = 0; i < goods_selected.length; i++) {
            if (goods_selected[i].ean_code == good.ean_code) {
                goods_selected.splice(i, 1);
            }
        }
    }

    updateGoodsInPackageStatus();
}

function goodsminus(goods_id, good) {
    var num = parseInt($("#" + goods_id).text());
    num -= good.sale_unit;

    if (num >= 0) {
        $("#" + goods_id).text(num);
        updateGoodSelected(goods_id, good, num);
    } else {
        bootbox.alert('数量已经为0');
    }
}

function goodsplus(goods_id, good, package_info) {
    var num = parseInt($("#" + goods_id).text());
    num += good.sale_unit;

    if (isGoodsInPackageValid(package_info, good, num)) {
        $("#" + goods_id).text(num);
        updateGoodSelected(goods_id, good, num);
    } else {
        bootbox.alert('超出海关限制，不能继续添加此物品！');
    }
}

function isGoodsInPackageValid(package_info, g, num) {
    var total_num = 0;
    var total_weight = 0;
    var total_value = 0;

    total_num += num;
    total_weight += g.brutto_weight * num;
    total_value += g.sale_price * num;

    for (var i = 0; i < goods_selected.length; i++) {
        var good = goods_selected[i];
        if (good._id != g._id) {
            total_num += good.num;
            total_weight += good.brutto_weight * good.num;
            total_value += good.sale_price * good.num;
        }
    }

    if (total_num > package_info.max_units) {
        return false;
    }

    if (total_value > package_info.max_value) {
        return false;
    }

    return true;

}

function updateGoodsInPackageStatus() {
    var total_num = 0;
    var total_weight = 0;
    var goods_value = 0;
    var baoyou_goods_weight = 0;
    var custom_fee = 0;
    var logistic_fee = 0;

    for (var i = 0; i < goods_selected.length; i++) {
        var good = goods_selected[i];
        total_num += good.num;
        total_weight += good.brutto_weight * good.num;
        goods_value += good.sale_price * good.num;

        if (good.custom_tax == 0) {
            baoyou_goods_weight += good.brutto_weight * good.num;
        } else {
            custom_fee += good.sale_price * good.num * good.custom_tax;
        }
    }

    /**
    if (baoyou_goods_weight > 0 ) {
        if (baoyou_goods_weight > 3.5) {
            logistic_fee = (total_weight - 6.5) * 20 > 0? (total_weight - 6.5) * 20 : 0;
        } else {
            logistic_fee = (total_weight - 3.5) * 20 > 0? (total_weight - 3.5) * 20 : 0;
        }
    } else {
        logistic_fee = total_weight * 20;
    }
     */

    var total_value = goods_value + custom_fee+ logistic_fee;


    $("#amount-items-added").text(total_num);
    $("#weight-items-total").text(total_weight.toFixed(2));
    $("#goods-value-total").text(goods_value.toFixed(2));
    $("#custom-value-total").text(custom_fee.toFixed(2));
    $("#package-value-total").text(logistic_fee.toFixed(2));
    $("#value-items-total").text(total_value.toFixed(2));

}

function submitpackage(element) {
    element.disabled = true;

    var is_receiver_save = $('#is_receiver_save').is(':checked') ? 1 : 0;
    var is_sender_save = $('#is_sender_save').is(':checked') ? 1 : 0;
    var customer_reference_no = $('#customer_reference_no').val();

    var receiver_name = $("#receiver_name").val();
    var receiver_identity = $("#receiver_identity").val();
    var receiver_tel = $("#receiver_tel").val();
    var province = $("#province").val();
    var city = $("#city").val();
    var district = $("#district").val();
    var receiver_street = $("#receiver_street").val();
    var receiver_postcode = $("#receiver_postcode").val();

    var sender_name = $("#sender_name").val();
    var sender_tel = $("#sender_tel").val();
    var sender_email = $("#sender_email").val();
    var sender_adr_str = $("#sender_adr_str").val();
    var sender_adr_str_no = $("#sender_adr_str_no").val();
    var sender_adr_plz = $("#sender_adr_plz").val();
    var sender_adr_city = $("#sender_adr_city").val();

    var package_weight = $("#weight-items-total").text();
    var packet_comment = $("#packet_comment").val();
    var total_fee = $("#value-items-total").text();
    var logistic_fee = $("#package-value-total").text();
    var custom_fee = $("#custom-value-total").text();
    var goods_fee = $("#goods-value-total").text();


    if (total_fee == 0) {
        bootbox.alert('请选择产品！', function () {
            element.disabled = false;
        });
        return;
    }

    to_check_ids = ['receiver_name', 'receiver_identity', 'receiver_tel',
        'province', 'city', 'district', 'receiver_street', 'receiver_postcode', 'sender_name',
        'sender_tel', 'sender_email', 'sender_adr_str', 'sender_adr_str_no', 'sender_adr_plz', 'sender_adr_city'];

    if (!elementCheckList(to_check_ids)) {
        bootbox.alert('您输入的信息有误， 请检查！', function () {
            element.disabled = false;
        });
        return;
    }

    if (goods_selected.length == 0) {
        bootbox.alert('请选择添加商品', function () {
            element.disabled = false;
        });
        return;
    }

    var package = {
        'pack': {
            'is_receiver_save': is_receiver_save,
            'is_sender_save': is_sender_save,
            'customer_reference_no': customer_reference_no,
            "receiver_name": receiver_name,
            "receiver_identity": receiver_identity,
            "receiver_tel": receiver_tel,
            "receiver_province": province,
            "receiver_city": city,
            "receiver_district": district,
            "receiver_street": receiver_street,
            "receiver_postcode": receiver_postcode,
            "sender_name": sender_name,
            "sender_tel": sender_tel,
            "sender_email": sender_email,
            "sender_street": sender_adr_str,
            "sender_hausnr": sender_adr_str_no,
            "sender_postcode": sender_adr_plz,
            "sender_city": sender_adr_city,
            "package_weight": package_weight,
            "comment": packet_comment.trim(),
            'package_custom_fee': custom_fee,
            'package_logistic_fee': logistic_fee,
            'package_goods_fee': goods_fee,
            'package_total_fee': total_fee
        },
        "goods": goods_selected
    };

    run_waitMe($("#packagesinglepage"), '提交中，请等待。。。。');

    if ($("#package_id").length) {

        var pid = $("#package_id").val();
        postsubmit('/onlineorder?pid=' + pid, JSON.stringify(package), function (response) {

            $("#packagesinglepage").waitMe('hide');
            if (response.status == 200) {
                bootbox.alert(response.msg, function () {
                    loadSubPage("ordertopay");
                });
            } else {
                bootbox.alert(response.msg);
            }
            element.disabled = false;
        });

    } else {
        postsubmit('/onlineorder', JSON.stringify(package), function (response) {
            $("#packagesinglepage").waitMe('hide');

            if (response.status == 200) {
                bootbox.alert(response.msg, function () {
                    loadSubPage("ordertopay");
                });
            } else {
                bootbox.alert(response.msg);
            }
            element.disabled = false;
        });

    }
}