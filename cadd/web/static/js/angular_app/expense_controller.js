function get_expense_head_list($scope, $http) {
    $http.get('/expense/expense_head_list/').success(function(data)
    {
        $scope.expense_heads = data.expense_heads;
        $scope.expense_head = 'select';
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}
function get_expense_list($scope, $http) {
    $http.get('/expense/expense_list/').success(function(data)
    {
        $scope.expenses = data.expenses;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function ExpenseController($scope, $element, $http, $timeout, $location) {

    $scope.expense =  {
        'expense_head_id': 'select',
        'voucher_no': '',
        'cheque_no': '',
        'cheque_date': '',
        'date': '',
        'payment_mode': 'cash',
        'narration': '',
        'branch': '',
        'bank_name': '',
        'amount': 0,
    }
    $scope.expense_heads = [];
    $scope.expense_head = '';
    
    $scope.payment_mode_selection = true;
    $scope.is_valid = false;
    $scope.error_flag = false;
    $scope.error_message = '';

    $scope.init = function(csrf_token, expense_id)
    {
        $scope.csrf_token = csrf_token;
        get_expense_head_list($scope, $http);
        var date_picker = new Picker.Date($$('#date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        if (expense_id) {
            $http.get('/expense/edit_expense/?expense_id='+expense_id).success(function(data){
                $scope.expense = data.expense[0];
                $scope.payment_mode_change($scope.expense.payment_mode);

            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
        get_expense_list($scope, $http);
    }
    $scope.payment_mode_change = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        } else {
            $scope.payment_mode_selection = true;
        }
    }
    $scope.add_expense_head = function() {
        $scope.head_name = '';
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '36%',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#add_expense_head'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
        $scope.error_message = '';
    }

    $scope.add_head = function(){
        if ($scope.head_name == '' || $scope.head_name == undefined) {
            $scope.message = 'Please enter Head Name';
        } else {
            $scope.message = '';
            params = { 
                'head_name': $scope.head_name,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expense/new_expense_head/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                if (data.result == 'error') {
                    $scope.message = data.message;
                } else {
                    $scope.message = '';
                    get_expense_head_list($scope, $http);
                    $scope.expense.expense_head_id = data.head_id;
                    $scope.close_popup();
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
    $scope.form_validation = function(){
        $scope.expense.voucher_no = $$('#voucher_no')[0].get('value');
        $scope.expense.date = $$('#date')[0].get('value');
        $scope.expense.cheque_date = $$('#cheque_date')[0].get('value');
        
        if ($scope.expense.expense_head_id == '' || $scope.expense.expense_head_id == undefined || $scope.expense.expense_head_id == 'select') {
            $scope.error_flag = true;
            $scope.error_message = 'Please choose Expense Head';
            return false;
        } else if ($scope.expense.amount == '' || $scope.expense.amount == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please enter amount';
            return false;
        } else if ($scope.expense.amount != Number($scope.expense.amount)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please enter valid amount';
            return false;
        } else if ($scope.expense.narration == '' || $scope.expense.narration == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add narration';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.cheque_no == '' || $scope.expense.cheque_no == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque no';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.cheque_date == '' || $scope.expense.cheque_date == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque date';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.bank_name == '' || $scope.expense.bank_name == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add bank name';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.branch == '' || $scope.expense.branch == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add branch';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.branch == '' || $scope.expense.branch == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add branch';
            return false;
        }
        return true;
    }
    $scope.save_expense = function(){
        if ($scope.form_validation()) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'expense': angular.toJson($scope.expense),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expense/new_expense/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.error_message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.error_message = '';
                    document.location.href ='/expense/new_expense/';
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
    $scope.edit_expense = function(){
        if ($scope.expense.cheque_date == null) {
            $scope.expense.cheque_date = ''
        }
        if ($scope.expense.cheque_no == null) {
            $scope.expense.cheque_no = ''
        }
        if ($scope.expense.branch == null) {
            $scope.expense.branch = ''
        } 
        if ($scope.expense.bank_name == null) {
            $scope.expense.bank_name = ''
        }
        if ($scope.form_validation()) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'expense': angular.toJson($scope.expense),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expense/edit_expense/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.error_message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.error_message = '';
                    document.location.href ='/expense/expense_list/';
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
}
function ExpenseReportController($scope, $http) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        var paid_date = new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var paid_date = new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.generate = function() {
        start_date = $('#start_date')[0].get('value');
        end_date = $('#end_date')[0].get('value');
        $scope.error_message = '';
        if (start_date == '' || start_date == undefined) {
            $scope.error_message = 'Please choose the start date';
        } else if (end_date == '' || end_date == undefined) {
            $scope.error_message = 'Please choose the end date';
        } else {
            document.location.href = '/expense/expense_report/?start_date='+start_date+'&end_date='+end_date;
        }
    }
}