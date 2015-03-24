
function get_receipt_no($scope, $http){
    $http.get('/fees/receipt_no/?ajax=true').success(function(data){
        $scope.payment_installment.receipt_no = data.receipt_no;
    }).error(function(data, status){
        $scope.message = data.result;
    })
}
function FeesPaymentController($scope, $element, $http, $timeout, share, $location)
{
    $scope.payment_installment = {
        'receipt_no': '',
        'installment_id': '',
        'course_id': '',
        'batch_id': '',
        'student_id': '',
        'head_id': '',
        'paid_date': '',
        'total_amount': '',
        'old_balance': 0,
        'paid_amount': 0,
        'paid_installment_amount': '',
        'balance': '',
        'student_fee_amount': '',
        'paid_fine_amount': '0',
        'fee_waiver': '0',
    }
    $scope.course = '';
    $scope.payment_installment.student = '';
    $scope.head = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        var paid_date = new Picker.Date($$('#paid_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_course_list($scope, $http);
        get_receipt_no($scope, $http);
    }
    $scope.get_student_list = function(){
        get_course_batch_student_list($scope, $http);
    }
    $scope.get_fees_head = function(){
        $scope.url = '/fees/get_fee_structure_head/'+ $scope.course+ '/'+ $scope.batch+ '/'+$scope.payment_installment.student+'/';
        if ($scope.course !='select' && $scope.batch != 'select' && $scope.payment_installment.student != 'select')
            $http.get($scope.url).success(function(data)
            {
                $scope.heads = data.heads;
                $scope.installments = [];
                $scope.payment_installment.amount = '';
                $scope.payment_installment.due_date = '';
                $scope.payment_installment.fine = '';
                $('#balance').val(0);
                $('#total_fee_amount').val(0);
                if ($scope.heads.length == 0) {
                    $scope.no_head_error = 'No fees structure for this batch';
                } else {
                    $scope.no_head_error = '';
                }
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
    }
    $scope.get_installment = function() {
        $scope.payment_installment.student = $scope.student.id;
        $scope.payment_installment.student_fee_amount = $scope.student.fees;
        $http.get('/admission/get_installment_details/?student='+$scope.payment_installment.student).success(function(data){
            if (data.installments.length == 0)
                $scope.no_installment_error = 'Payment completed';
            else
                $scope.no_installment_error = '';
            $scope.installments = data.installments;
            console.log($scope.installments);
            $('#due_date').val('');
            $('#fine_amount').val(0);
            $('#fee_amount').val(0);
            $('#total_fee_amount').val(0);
        }).error(function(data, status){
            console.log('Request failed', data);
        })
    }
    $scope.calculate_total_amount = function() {
        console.log("hsahii")
        calculate_total_fee_amount('create');
    }
    $scope.get_fees = function(installment) {
        $scope.payment_installment.paid_date = installment.paid_date;
        $scope.payment_installment.due_date = installment.due_date;
        $scope.payment_installment.amount = installment.amount;
        $scope.payment_installment.fine = installment.fine_amount;
        $scope.payment_installment.paid_installment_amount = installment.paid_installment_amount;
        $scope.payment_installment.balance = installment.balance;
        $scope.payment_installment.total_amount_paid = installment.total_amount_paid;
        // $scope.payment_installment.installment_balance = $scope.payment_installment.amount - $scope.payment_installment.paid_installment_amount;
        $('#due_date').val(installment.due_date);
        $('#fine_amount').val(installment.fine_amount);
        $('#fee_amount').val(installment.amount);
        $('#balance').val(installment.balance);
        balance = 0;
        balance = $scope.payment_installment.amount - $scope.payment_installment.paid_installment_amount;
        if (balance<0)
            balance = 0;
        $('#installment_balance').val(balance);
        $('#installment_balance_amount').val($scope.payment_installment.amount - $scope.payment_installment.paid_installment_amount);
        $scope.payment_installment.total_balance = installment.course_balance;
        $scope.payment_installment.total_balance_amount = installment.course_balance;
        if ((parseFloat($scope.payment_installment.total_balance) - parseFloat($scope.payment_installment.amount))>0)
            $('#old_balance').val(parseFloat($scope.payment_installment.total_balance) - parseFloat($scope.payment_installment.amount));
        else
            $('#old_balance').val(0);
        calculate_total_fee_amount('create');
    }
    $scope.calculate_balance = function() {
        balance = 0;
        balance = parseFloat($('#total_fee_amount').val()) - (parseFloat($scope.payment_installment.paid_amount) + parseFloat($scope.payment_installment.paid_installment_amount) + parseFloat($scope.payment_installment.paid_fine_amount));
        if (balance < 0)
            balance =0;
        $('#installment_balance').val(balance);
        balance = parseFloat($('#installment_balance').val()) - parseFloat($scope.payment_installment.fee_waiver);
        if (balance < 0)
            balance =0;
        $('#installment_balance').val(balance);
        $scope.payment_installment.total_balance = parseFloat($scope.payment_installment.total_balance_amount) - (parseFloat($scope.payment_installment.paid_amount));
        $scope.payment_installment.total_balance = parseFloat($scope.payment_installment.total_balance) - parseFloat($scope.payment_installment.fee_waiver)
        
    }
    $scope.validate_fees_payment = function() {
        $scope.validation_error = '';

        var fine_balance = parseFloat($('#total_fee_amount').val()) - parseFloat($scope.payment_installment.amount);
        if($scope.course == '' || $scope.course == undefined) {
            $scope.validation_error = "Please Select a course " ;
            return false
        } else if($scope.payment_installment.student == '' || $scope.payment_installment.student == undefined) {
            $scope.validation_error = "Please select a student" ;
            return false;
        } else if($scope.installments.length == 0) {
            $scope.validation_error = "Payment completed" ;
            return false;
        } else if($scope.installment == '' || $scope.installment == undefined) {
            $scope.validation_error = "Please choose an installment" ;
            return false;
        } else if ($scope.payment_installment.paid_amount == '' || $scope.payment_installment.paid_amount == undefined) {
            $scope.validation_error = "Please enter paid amount" ;
            return false;
        } else if($scope.payment_installment.fee_waiver == ''){
            $scope.validation_error = "Please enter a valid amount in fee waiver" ;
            return false;
        } else if ($scope.payment_installment.paid_amount != Number($scope.payment_installment.paid_amount)) {
            $scope.validation_error = "Please enter valid paid amount" ;
            return false;
        } else if (fine_balance < $scope.payment_installment.paid_fine_amount ) {
            $scope.validation_error = "Please check the Paying Fine amount";
            return false;
        } else if ($scope.payment_installment.installment_balance < 0 ) {
            $scope.validation_error = "Please check the Paying amount";
            return false;
        } else if($scope.payment_installment.paid_fine_amount == ''){
            $scope.validation_error = "Please enter a valid amount in fine amount" ;
            return false;
        } return true; 
        // else if ($scope.payment_installment.paid_amount != $scope.payment_installment.balance) {
        //     $scope.validation_error = "Please check the balance amount with paid amount" ;
        //     return false;
        // } 
    }
    $scope.save_fees_payment = function() {

        $scope.payment_installment.course_id = $scope.course;
        $scope.payment_installment.installment_id = $scope.installment;
        $scope.payment_installment.paid_date = $$('#paid_date')[0].get('value');
        // $scope.payment_installment.total_amount = $$('#total_fee_amount')[0].get('value');
        $scope.payment_installment.total_amount = $$('#fee_amount')[0].get('value');
        $scope.payment_installment.installment_balance = $$('#installment_balance')[0].get('value');
        if($scope.validate_fees_payment()) {
            params = { 
                'fees_payment': angular.toJson($scope.payment_installment),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method: 'post',
                url: "/fees/fees_payment/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {              
                    document.location.href ="/fees/fees_payment/";
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}
function EditFeesPaymentController($scope, $element, $http, $timeout, share, $location)
{
    $scope.payment_details = {
        'receipt_no': '',
        'installment_id': '',
        'course_id': '',
        'batch_id': '',
        'student_id': '',
        'paid_date': '',
        'total_amount': '',
        'old_balance': 0,
        'paid_amount': 0,
        'paid_amount': '',
        'due_date' : '',
        'balance': '',
        'balance': '',
        'student_fee_amount': '',
        'paid_fine_amount': '0',
        'fee_waiver': '0',
    }
    $scope.course = '';
    $scope.payment_details.student = '';
    $scope.head = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        var paid_date = new Picker.Date($$('#paid_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            onSelect: $scope.calculate_total_amount('edit'),
        });
        $scope.calculate_total_amount('edit');
        
    }
    $scope.get_fees_payment_details = function(){
        var url = '/fees/get_fees_payment/?receipt_no='+$scope.receipt_no;
        $http.get(url).success(function(data) {
            if (data.result == 'ok'){
                $scope.payment_details = '';
                $scope.validation_error = '';
                $scope.payment_details = data.payment_details;
                $scope.get_fees();
            }
            else{
                $scope.validation_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    
    $scope.calculate_total_amount = function() {
        console.log('Hiisss')
        calculate_total_fee_amount('edit');
    }
    $scope.get_fees = function() {
        // $scope.payment_installment.installment_balance = $scope.payment_installment.amount - $scope.payment_installment.paid_installment_amount;
        $('#due_date').val($scope.payment_details.due_date);
        $('#paid_date').val($scope.payment_details.paid_date);
        $('#fine_amount').val($scope.payment_details.fine_amount);
        $('#fee_amount').val($scope.payment_details.installment_amount);
        $('#balance').val($scope.payment_details.balance);
        balance = 0;
        balance = $scope.payment_details.installment_amount - $scope.payment_details.paid_amount;
        if (balance<0)
            balance = 0;
        $('#installment_balance').val(balance);
        $('#installment_balance_amount').val($scope.payment_details.installment_amount - $scope.payment_details.paid_amount);
        $scope.payment_details.total_balance = $scope.payment_details.balance;
        $scope.payment_details.total_balance_amount = $scope.payment_details.balance;
        $scope.payment_details.paying_amount = $scope.payment_details.paid_amount;
        // $scope.payment_details.total_installment_amount = $scope.payment_details.paid_amount + $scope.payment_details.fine;
        calculate_total_fee_amount('edit');
    }
    $scope.calculate_balance = function() {
        balance = 0;
        balance = parseFloat($('#total_fee_amount').val()) - (parseFloat($scope.payment_details.paid_amount) + parseFloat($scope.payment_details.paid_fine_amount));
        
        if (balance < 0)
            balance =0;
        $('#installment_balance').val(balance);
        balance = parseFloat($('#installment_balance').val()) - parseFloat($scope.payment_details.fee_waiver);
        if (balance < 0)
            balance =0;
        $('#installment_balance').val(balance);
        $scope.payment_details.installment_balance = parseFloat($scope.payment_details.installment_amount) - parseFloat($scope.payment_details.paid_amount);
        $scope.payment_details.total_balance = parseFloat($scope.payment_details.total_balance_amount)+  parseFloat($scope.payment_details.paying_amount) - (parseFloat($scope.payment_details.paid_amount));
        $scope.payment_details.total_balance = parseFloat($scope.payment_details.total_balance) - parseFloat($scope.payment_details.fee_waiver)
        
    }
    $scope.validate_fees_payment = function() {
        $scope.validation_error = '';

        var fine_balance = parseFloat($('#total_fee_amount').val()) - parseFloat($scope.payment_details.amount);
        if ($scope.payment_details.paid_amount == '' || $scope.payment_details.paid_amount == undefined) {
            $scope.validation_error = "Please enter paid amount" ;
            return false;
        } else if($scope.payment_details.fee_waiver == ''){
            $scope.validation_error = "Please enter a valid amount in fee waiver" ;
            return false;
        } else if ($scope.payment_details.paid_amount != Number($scope.payment_details.paid_amount)) {
            $scope.validation_error = "Please enter valid paid amount" ;
            return false;
        } else if (fine_balance < $scope.payment_details.paid_fine_amount ) {
            $scope.validation_error = "Please check the Paying Fine amount";
            return false;
        } else if ($scope.payment_details.installment_balance < 0 ) {
            $scope.validation_error = "Please check the Paying amount";
            return false;
        } else if($scope.payment_details.paid_fine_amount == ''){
            $scope.validation_error = "Please enter a valid amount in fine amount" ;
            return false;
        } return true; 
        // else if ($scope.payment_installment.paid_amount != $scope.payment_installment.balance) {
        //     $scope.validation_error = "Please check the balance amount with paid amount" ;
        //     return false;
        // } 
    }
    $scope.save_fees_payment = function() {

        // $scope.payment_details.course_id = $scope.course;
        // $scope.payment_details.installment_id = $scope.installment;
        $scope.payment_details.paid_date = $$('#paid_date')[0].get('value');
        // $scope.payment_installment.total_amount = $$('#total_fee_amount')[0].get('value');
        // $scope.payment_details.total_amount = $$('#fee_amount')[0].get('value');
        // $scope.payment_details.installment_balance = $$('#installment_balance')[0].get('value');
        if($scope.validate_fees_payment()) {
            params = { 
                'fees_payment': angular.toJson($scope.payment_details),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method: 'post',
                url: "/fees/edit_fees/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {              
                    document.location.href ="/fees/edit_fees/";
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}
function FeesController($scope, $element, $http, $timeout, share, $location)
{
    $scope.student_id = '';
    $scope.course = '';
    $scope.batch = '';
    $scope.fees_type = '';
    $scope.filtering_option = '';
    $scope.url = '';
    $scope.date = '';
    $scope.show_student_wise_report = false;
    $scope.show_date_wise_report = false;

    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';
        var date = new Picker.Date($$('#date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_course_list($scope, $http);
    }
    $scope.get_batch = function(){
        $scope.filtering_option = '';
        get_course_batch_list($scope, $http);
    }
    $scope.get_student = function(){
        $scope.fees_details = [];
        $scope.filtering_option = '';
        get_course_batch_student_list($scope, $http);
    }
    $scope.change_report_type = function(report_type){
        if(report_type == 'date_wise') {
            $scope.show_student_wise_report = false;
            $scope.show_date_wise_report = true;
        }else{
            $scope.show_student_wise_report = true;
            $scope.show_date_wise_report = false;
        }
    }
    $scope.hide_popup_windows = function(){
        $('#fees_structure_details_view')[0].setStyle('display', 'none');
    }
    $scope.select_page = function(page){
        select_page(page, $scope.fees_details.students, $scope, 2);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.outstanding_fees_details = function(){ 
        $scope.url = '';
        if (($scope.fees_type != '' || $scope.fees_type != undefined) && ($scope.filtering_option != '' || $scope.filtering_option != undefined)) {
            if ($scope.course != 'select' && $scope.batch != 'select') {
                // if ($scope.filtering_option == 'student_wise' && $scope.student_id != 'select') {
                //     $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course+ '&batch='+ $scope.batch+ '&student_id='+$scope.student_id+'&filtering_option='+$scope.filtering_option+'&fees_type='+$scope.fees_type;
                // } else {
                //     $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course+ '&batch='+ $scope.batch+ '&filtering_option='+$scope.filtering_option+'&fees_type='+$scope.fees_type;
                // }
                if($scope.course != '' && $scope.student_id != '')
                    $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course+'&student_id='+$scope.student_id;

            }
        }
        $http.get($scope.url).success(function(data)
        {
            if (data.result == 'ok') {
                if (data.fees_details.length > 0) {
                    $scope.fees_details = data.fees_details[0];
                    if($scope.fees_details.students)
                        paginate($scope.fees_details.students, $scope, 2);
                } else {
                    $scope.fees_details = [];
                    $scope.fees_details.roll_no = data.roll_no
                    $scope.fees_details.student_name = data.student_name
                }
            } else {
                $scope.no_student_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }    
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }   
    $scope.print_outstanding_fees_list = function() {
        $scope.date = $$('#date')[0].get('value');
        if ($scope.student_id)
            document.location.href = '/fees/print_outstanding_fees_details/?student='+$scope.student_id;
        else if($scope.date)
           document.location.href = '/fees/print_outstanding_fees_details/?date='+$scope.date;
    }
}

function FeesPaymentReportController($scope, $http, $element) {
    $scope.report_type = '';
    $scope.date = '';
    $scope.show_course_wise_report = false;
    $scope.show_student_wise_report = false;
    $scope.show_date_wise_report = false;
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.focusIndex < $scope.students_list.length-1){
            $scope.focusIndex++; 
        }
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        var start_date = new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var end_date = new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var course_start_date = new Picker.Date($$('#course_start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var course_end_date = new Picker.Date($$('#course_end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_course_list($scope, $http);
    }
    $scope.select_list_item = function(index){
        student = $scope.students_list[index];
        $scope.get_report('student_wise',student);
    }
    $scope.change_report_type = function(report_type){
        if (report_type == 'course_wise'){
            $scope.show_course_wise_report = true;
            $scope.show_student_wise_report = false;
            $scope.show_date_wise_report = false;
        }else if(report_type == 'date_wise') {
            $scope.show_student_wise_report = false;
            $scope.show_course_wise_report = false;
            $scope.show_date_wise_report = true;
        }else{
            $scope.show_student_wise_report = true;
            $scope.show_course_wise_report = false;
            $scope.show_date_wise_report = false;
        }
    }
    $scope.student_search = function(){
        if($scope.student_name.length > 0){
            $scope.validation_error = "";
            student_search($scope, $http);
        }
        else
            $scope.students_list = ""
    }
    $scope.get_report = function(report_type,student){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        $scope.course_start_date = $$('#course_start_date')[0].get('value');
        $scope.course_end_date = $$('#course_end_date')[0].get('value');
        if (report_type == 'student_wise') {
            document.location.href = '/fees/fees_payment_report/?&student_id='+student.id+'&report_type='+report_type;
        }else if(report_type == 'course_wise'){
            document.location.href = '/fees/fees_payment_report/?course='+$scope.course+'&start_date=' +$scope.course_start_date+ '&end_date=' +$scope.course_end_date + '&report_type='+report_type;
        }else if(report_type == 'date_wise'){
            document.location.href = '/fees/fees_payment_report/?start_date='+$scope.start_date+ '&end_date=' +$scope.end_date +'&report_type='+report_type;
        }
    }
}
function UnRollController($scope, $http, $element) {
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.unroll_student_flag = true;
        $scope.roll_student_flag = true;
        get_course_list($scope, $http);
    }
    $scope.get_outstanding_student = function(){
        $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course;
        $http.get($scope.url).success(function(data)
        {
            if (data.result == 'ok') {
                if (data.fees_details.length > 0) {
                    $scope.fees_details = data.fees_details[0];
                    if ($scope.fees_details.student_details.length == 0) {
                        $scope.no_student_error = "No students"
                    }
                    for(i=0;i<$scope.fees_details.student_details.length;i++){
                        $scope.no_student_error = '';
                        if($scope.fees_details.student_details[i].is_rolled == 'false'){
                            $scope.fees_details.student_details[i].is_rolled = false;
                            $scope.fees_details.student_details[i].is_unrolled = true;
                            // $scope.unroll_student_flag = true;
                        }else if($scope.fees_details.student_details[i].is_rolled == 'true'){
                            $scope.fees_details.student_details[i].is_unrolled = false;
                            $scope.fees_details.student_details[i].is_rolled = true;
                            // $scope.roll_student_flag = true;
                        }
                    }
                    // if($scope.fees_details.students)
                    //     paginate($scope.fees_details.students, $scope, 2);
                } else {
                    $scope.fees_details = [];
                    $scope.no_student_error = "No students"
                }
            } else {
                $scope.no_student_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.unroll = function(student){
        // $scope.roll_student_flag = false;
        $scope.student_id = student.student_id;
        student.is_rolled = true;
        student.is_unrolled = false;
        $scope.url = '/fees/unroll_students/?student_id='+$scope.student_id;
        $http.get($scope.url).success(function(data)
        {
            if (data.result == 'ok') {
                
            } else {
                $scope.no_student_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.roll = function(student){
        student.is_unrolled = true;
        student.is_rolled = false;
        // $scope.unroll_student_flag = false;
        $scope.student_id = student.student_id;
        $scope.url = '/fees/roll_students/?student_id='+$scope.student_id;
        $http.get($scope.url).success(function(data)
        {
            if (data.result == 'ok') {
                
            } else {
                $scope.no_student_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}
function AccountStatementController($scope, $http, $element) {
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.focusIndex < $scope.students_list.length-1){
            $scope.focusIndex++; 
        }
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
    }
    $scope.select_list_item = function(index){
        student = $scope.students_list[index];
        $scope.get_student(student);
    }
    
    $scope.student_search = function(){
        if($scope.student_name.length > 0){
            $scope.validation_error = "";
            student_search($scope, $http);
        }
        else
            $scope.students_list = ""
    }
    $scope.get_student = function(student){
        $scope.student_name = student.name;
        $scope.student = student.id;
        $scope.students_list = {};
    }
    $scope.get_report = function(){
       
        document.location.href = '/fees/account_statement/?&student_id='+$scope.student;
    }
}