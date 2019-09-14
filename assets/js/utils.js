function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

getFormJsonAndAction = function (formid, callback) {
    var formAction = $('#' + formid).attr('action');
    var jsonbody = {};
    var set = $('#' + formid + ' :input');
    $('#' + formid + ' :input').each(
        function (index) {
            var input = $(this);
            jsonbody[input.attr('name')] = input.val();
            var isLastElement = index == set.length - 1;

            if (isLastElement) {
                callback(formAction, jsonbody);
            }
        }
    );
};

function sendFormJsonToServer(formid, callback) {
    $('#' + formid).submit(function (event) {
        event.preventDefault(); //prevent default action
        getFormJsonAndAction(formid, function (formaction, jsonbody) {
            postsubmit(formaction, JSON.stringify(jsonbody), function (data) {
                if (callback) {
                    callback(data);
                } else {
                    alert(JSON.stringify(data));
                }
            });
        });
    });
}

function sendJsonToServer(elements, url, callback) {
    var jsonbody = {};
    for (var i = 0; i < elments.length; i++) {
        var input = $('#' + elements[0]);
        jsonbody[input.attr('name')] = input.val();
    }

    postsubmit(url, JSON.stringify(jsonbody), function (data) {
        if (callback) {
            callback(data);
        } else {
            alert(JSON.stringify(data));
        }
    });
}

function postsubmit(formaction, jsonbody, callback, datetype) {
    datetype = datetype || 'json';
    $.ajax({
        url: formaction,
        type: "POST",
        dataType: datetype,
        data: jsonbody,
        success: function (data) {
            callback(data);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
            alert(thrownError);
        }
    });
}

// 身份证号码的验证规则
function isIdCardNo(idcard) {
    idcard = idcard.toString();
    //var Errors=new Array("验证通过!","身份证号码位数不对!","身份证号码出生日期超出范围或含有非法字符!","身份证号码校验错误!","身份证地区非法!");
    var Errors = new Array(true, false, false, false, false);
    var area = {
        11: "北京",
        12: "天津",
        13: "河北",
        14: "山西",
        15: "内蒙古",
        21: "辽宁",
        22: "吉林",
        23: "黑龙江",
        31: "上海",
        32: "江苏",
        33: "浙江",
        34: "安徽",
        35: "福建",
        36: "江西",
        37: "山东",
        41: "河南",
        42: "湖北",
        43: "湖南",
        44: "广东",
        45: "广西",
        46: "海南",
        50: "重庆",
        51: "四川",
        52: "贵州",
        53: "云南",
        54: "西藏",
        61: "陕西",
        62: "甘肃",
        63: "青海",
        64: "宁夏",
        65: "新疆",
        71: "台湾",
        81: "香港",
        82: "澳门",
        91: "国外"
    }
    var idcard, Y, JYM;
    var S, M;
    var idcard_array = new Array();
    idcard_array = idcard.split("");
    //地区检验
    if (area[parseInt(idcard.substr(0, 2))] == null) return Errors[4];
    //身份号码位数及格式检验
    switch (idcard.length) {
        case 18:
            //18 位身份号码检测
            //出生日期的合法性检查
            //闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
            //平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
            if (parseInt(idcard.substr(6, 4)) % 4 == 0 || (parseInt(idcard.substr(6, 4)) % 100 == 0 && parseInt(idcard.substr(6, 4)) % 4 == 0)) {
                ereg = /^[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$/;//闰年出生日期的合法性正则表达式
            } else {
                ereg = /^[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$/;//平年出生日期的合法性正则表达式
            }
            if (ereg.test(idcard)) {//测试出生日期的合法性
                //计算校验位
                S = (parseInt(idcard_array[0]) + parseInt(idcard_array[10])) * 7
                    + (parseInt(idcard_array[1]) + parseInt(idcard_array[11])) * 9
                    + (parseInt(idcard_array[2]) + parseInt(idcard_array[12])) * 10
                    + (parseInt(idcard_array[3]) + parseInt(idcard_array[13])) * 5
                    + (parseInt(idcard_array[4]) + parseInt(idcard_array[14])) * 8
                    + (parseInt(idcard_array[5]) + parseInt(idcard_array[15])) * 4
                    + (parseInt(idcard_array[6]) + parseInt(idcard_array[16])) * 2
                    + parseInt(idcard_array[7]) * 1
                    + parseInt(idcard_array[8]) * 6
                    + parseInt(idcard_array[9]) * 3;
                Y = S % 11;
                M = "F";
                JYM = "10X98765432";
                M = JYM.substr(Y, 1);//判断校验位
                if (M == idcard_array[17]) return Errors[0]; //检测ID的校验位
                else return Errors[3];
            }
            else return Errors[2];
            break;
        default:
            return Errors[1];
            break;
    }
}

function elementCheckList(elments) {
    var is_validated = true;
    for (var i = 0; i < elments.length; i++) {
        if (!isElementValidated(elments[i])) {
            is_validated = false;
        }
    }

    return is_validated;
}

function isElementValidated(element_id) {
    var err = "";

    var input = $('#' + element_id);

    if (input.attr('type') != 'file') {
        input.removeClass('has-error').next('span').toggleClass('is-visible');
        input.next('span').removeClass('is-visible');

        var inpunt_length = 0;
        if (input.val()) {
            inpunt_length = input.val().length;
        }

        if (inpunt_length == 0) {
            err = "此选项不能为空";
        }

        if (input.attr("minlength") && inpunt_length < parseInt(input.attr("minlength"))) {
            err = "输入字符过少";
        }

        if (input.attr("maxlength") && inpunt_length > parseInt(input.attr("maxlength"))) {
            err = "输入字符过多";
        }

        if (input.attr("type") == 'number') {
            if (parseInt(input.val()) < 0) {
                err = "输入值不可为负数";
            }
            if (input.attr("min") && parseInt(input.val()) < parseInt(input.attr("min"))) {
                err = "输入值不能小于" + input.attr("min");
            }
        }


        if (input.attr("name") && input.attr("name").includes('receiver_identity') && !isIdCardNo(input.val())) {
            err = "身份证号码不正确";
        }


        if (err.length > 0) {
            input.toggleClass('has-error').next('span').text(err);
            input.toggleClass('has-error').next('span').toggleClass('is-visible');

            return false;
        }
    }
    return true;
}

function getBase64(file, callback) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        callback(reader.result);
    };
    reader.onerror = function (error) {
        alert('Error: ', error);
    };
}

function response_dialog(response, callback) {
    if (response.status == 200) {
        if (callback) {
            callback();
        }
    } else {
        bootbox.alert("操作失败!原因为：" + response.msg)
    }

}

function run_waitMe(el, text) {
    el.waitMe({
        effect: "bounce",
        text: text,
        bg: 'rgba(255,255,255,0.7)',
        color: '#000',
        maxSize: 30,
        waitTime: -1,
        source: "<svg width='48px' height='48px' xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\" preserveAspectRatio=\"xMidYMid\" class=\"uil-default\"><rect x=\"0\" y=\"0\" width=\"100\" height=\"100\" fill=\"none\" class=\"bk\"></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(0 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(30 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.08333333333333333s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(60 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.16666666666666666s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(90 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.25s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(120 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.3333333333333333s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(150 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.4166666666666667s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(180 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.5s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(210 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.5833333333333334s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(240 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.6666666666666666s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(270 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.75s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(300 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.8333333333333334s' repeatCount='indefinite'/></rect><rect x='46.5' y='40' width='7' height='20' rx='5' ry='5' fill='#00b2ff' transform='rotate(330 50 50) translate(0 -30)'> <animate attributeName='opacity' from='1' to='0' dur='1s' begin='0.9166666666666666s' repeatCount='indefinite'/></rect></svg>",
        textPos: 'vertical',
        onClose: function (el) {
        }
    });
}


function download(filename, type, base64) {
    var byteCharacters = atob(base64);
    var byteNumbers = new Array(byteCharacters.length);
    for (var i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    var data = new Uint8Array(byteNumbers);
    if (data != null && navigator.msSaveBlob)
        return navigator.msSaveBlob(new Blob([data], {type: type}), filename);
    var a = $("<a style='display: none;'/>");
    var url = window.URL.createObjectURL(new Blob([data], {type: type}));
    a.attr("href", url);
    a.attr("download", filename);
    $("body").append(a);
    a[0].click();
    window.URL.revokeObjectURL(url);
    a.remove();
}


function openmodal(modal_id) {
    $("#" + modal_id).modal();
}

loadSubPage=function (pagename) {
    $.get( '/' + pagename, function( response ) {
        $('#view').html(response);
    });
};