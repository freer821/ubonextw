function sendPersonID() {
    to_check_ids = ['package-code', 'person-id'];
    if (elementCheckList(to_check_ids)) {
        var file = document.getElementById('person-id').files[0];
        if (file) {
            getBase64(file, function (base64) {

                var jsonbody = {
                    'person-id': base64,
                    'package-code': $('#package-code').val()
                };

                postsubmit('/upload_identity', JSON.stringify(jsonbody), function (data) {
                    alert(JSON.stringify(data));
                });
            })
        } else {
            alert('请选择身份证照片')
        }

    }
}