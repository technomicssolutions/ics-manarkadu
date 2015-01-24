function get_staffs($scope, $http) {
    $http.get("/staff/staffs/").success(function(data)
    {
        $scope.staffs = data.staffs;
        paginate($scope.staffs, $scope);
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}
function validate_staff($scope) {
    $scope.validation_staff_error = '';
    $scope.staff.dob = $$('#dob')[0].get('value');
    $scope.staff.doj = $$('#doj')[0].get('value');
    if($scope.staff.first_name == '' || $scope.staff.first_name == undefined) {
        $scope.validation_staff_error = "Please Enter the First Name" ;
        return false;
    } else if($scope.staff.last_name == '' || $scope.staff.last_name == undefined) {
        $scope.validation_staff_error = "Please Enter the Last Name" ;
        return false;
    } else if($scope.new_staff && $scope.staff.username == '' || $scope.staff.username == undefined) {
        $scope.validation_staff_error = "Please Enter the Username" ;
        return false;
    } else if($scope.is_user_exists) {
        $scope.validation_staff_error = "Username already exists" ;
        return false;
    } else if($scope.new_staff == true &&($scope.staff.password == '' || $scope.staff.password == undefined)) {
        $scope.validation_staff_error = "Please Enter the Password" ;
        return false;
    } else if($scope.new_staff == true && ($scope.confirm_password == '' || $scope.confirm_password == undefined)) {
        $scope.validation_staff_error = "Please Enter the Confirm Password" ;
        return false;
    } else if($scope.new_staff == true && ($scope.staff.password != $scope.confirm_password)) {
        $scope.validation_staff_error = "Password not matches with Confirm Password" ;
        return false;
    } else if($scope.staff.dob == '' || $scope.staff.dob == undefined) {
        $scope.validation_staff_error = "Please Enter DOB";
        return false;
    } else if($scope.staff.address == '' || $scope.staff.address == undefined) {
        $scope.validation_staff_error = "Please Enter Address";
        return false;
    } else if($scope.staff.mobile_number == ''|| $scope.staff.mobile_number == undefined){
        $scope.validation_staff_error = "Please enter the Mobile Number";
        return false;
    } else if($scope.staff.mobile_number.length < 9 || $scope.staff.mobile_number.length > 15) {            
        $scope.validation_staff_error = "Please enter a Valid Mobile Number";
        return false;
    } else if($scope.staff.land_number == ''|| $scope.staff.land_number == undefined){
        $scope.validation_staff_error = "Please enter the Telephone Number";
        return false;
    } else if($scope.staff.land_number.length < 9 || $scope.staff.land_number.length > 15) {            
        $scope.validation_staff_error = "Please enter a Valid Telephone Number";
        return false;
    } else if(($scope.staff.email == '' || $scope.staff.email == undefined) || (!(validateEmail($scope.staff.email)))){
        $scope.validation_staff_error = "Please enter a Valid Email Id";
        return false;
    } else if($scope.staff.blood_group == '' || $scope.staff.blood_group == undefined) {
        $scope.validation_staff_error = "Please choose Blood Group";
        return false; 
    } else if($scope.staff.doj == '' || $scope.staff.doj == undefined) {
        $scope.validation_staff_error = "Please Enter Date of Join";
        return false;
    } else if($scope.staff.qualifications == '' || $scope.staff.qualifications == undefined) {
        $scope.validation_staff_error = "Please enter qualifications";
        return false; 
    } else if($scope.staff.experience == '' || $scope.staff.experience == undefined) {
        $scope.validation_staff_error = "Please enter experience";
        return false;
    } else if($scope.staff.role == '' || $scope.staff.role == undefined) {
        $scope.validation_staff_error = "Please enter role";
        return false;
    } 
    return true;
}
function save_staff($scope, $http, from) {
    if(validate_staff($scope)) {
        show_spinner();
        params = { 
            'staff': angular.toJson($scope.staff),
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        var fd = new FormData();
        if ($scope.photo_img != undefined)
            fd.append('photo_img', $scope.photo_img.src)
        for(var key in params){
            fd.append(key, params[key]);          
        }
        var url = "/staff/add_staff/";
        $http.post(url, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined
            }
        }).success(function(data, status){
            hide_spinner();
            if (data.result == 'error'){
                $scope.error_flag = true;
                $scope.message = data.message;
            } else {
                if (from == 'permission') {
                    $scope.close_popup();
                    $scope.select_staff(data.staff);
                } else 
                    document.location.href ="/staff/staffs/";
            }

        }).error(function(data, status){
            $scope.error_flag=true;
            $scope.message = data.message;
        });
    }
}
function StaffController($scope, $element, $http, $timeout, share, $location) {
    $scope.new_staff = false;
    $scope.staff = {
        'first_name': '',
        'last_name': '',
        'username': '',
        'password': '',
        'dob': '',
        'address': '',
        'mobile_number': '',
        'land_number': '',
        'email':'',
        'blood_group': '',
        'doj': '',
        'qualifications': '',
        'experience':'',
        'role': '',
    }
    $scope.is_user_exists = false;
    
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';
        get_staffs($scope, $http);
        var date_pick = new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#doj'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.select_page = function(page){
        select_page(page, $scope.staffs, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    } 
    $scope.add_new_staff = function(){  
        $scope.new_staff = true;
        $scope.staff = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password': '',
            'dob': '',
            'address': '',
            'mobile_number': '',
            'land_number': '',
            'email':'',
            'blood_group': '',
            'doj': '',
            'qualifications': '',
            'experience':'',
            'role': '',
        }
        $scope.popup = new DialogueModelWindow({   
            'dialogue_popup_width': '79%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_staff_details'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.is_username_exists = function() {
        var is_exists_url = '/staff/is_username_exists/?username='+$scope.staff.username;
        $http.get(is_exists_url).success(function(data){
            $scope.is_exist_message = '';
            if (data.result == 'error') {
                $scope.is_exist_message = data.message;
                $scope.is_user_exists = true;
            } else {
                $scope.is_user_exists = false;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.save_new_staff = function() {
        save_staff($scope, $http, 'staff');
    }
    $scope.edit_staff = function(staff) {
        $scope.new_staff = false;
        $scope.popup = new DialogueModelWindow({   
            'dialogue_popup_width': '79%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_staff_details'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
        $scope.staff = staff;
    }
}

function PermissionController($scope, $http) {
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.focusIndex < $scope.staffs.length-1){
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
    $scope.no_staff = false;
    $scope.permission = {
        'staff': '',
        'attendance_module': false,
        'student_module': false,
        'master_module': false,
        'fees_module': false,
        'register_module': false,
        'expense_module': false,
    }
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
    }
    $scope.search_staff = function() {
        $scope.permission.staff = '';
        $scope.staff_selected = true;
        $scope.no_staff = false;
        $scope.staffs = [];
        $scope.no_staff_message = '';
        if ($scope.staff_name.length > 0) {
            $http.get('/staff/staffs/?staff_name='+$scope.staff_name).success(function(data){
                $scope.staffs = data.staffs;
                if ($scope.staffs.length == 0) {
                    $scope.no_staff_message = 'No such staff';
                    $scope.no_staff = true;
                }
            }).error(function(data, status){
                console.log('Request failed' || data);
            })
        }
    }
    $scope.select_staff = function(staff) {
        $scope.staff_selected = false;
        $scope.staff_name = staff.first_name + ' ' + staff.last_name;
        $scope.permission.staff = staff.id;
        if (staff.permission.attendance_module == 'true')
            $scope.permission.attendance_module = true;
        else
            $scope.permission.attendance_module = false;
        if (staff.permission.student_module == 'true')
            $scope.permission.student_module = true;
        else
            $scope.permission.student_module = false;
        if (staff.permission.master_module == 'true')
            $scope.permission.master_module = true;
        else
            $scope.permission.master_module = false;
        if (staff.permission.fees_module == 'true')
            $scope.permission.fees_module = true;
        else
            $scope.permission.fees_module = false;
        if (staff.permission.register_module == 'true')
            $scope.permission.register_module = true;
        else
            $scope.permission.register_module = false;
        if (staff.permission.expense_module == 'true')
            $scope.permission.expense_module = true;
        else
            $scope.permission.expense_module = false;

        $scope.staffs = [];
    }
    $scope.select_list_item = function(index){
        staff = $scope.staffs[index];
        $scope.select_staff(staff);
    }
    $scope.save_permissions = function() {
        $scope.validate_staff_permission = '';
        if ($scope.permission.staff == '' || $scope.permission.staff == undefined) {
            $scope.validate_staff_permission = 'Please choose the Staff';
        } else if ($scope.no_staff_error) {
            $scope.validate_staff_permission = 'No such staff';
        } else {
            show_spinner();
            if ($scope.permission.attendance_module == true) {
                $scope.permission.attendance_module = 'true';
            } else {
                $scope.permission.attendance_module = 'false';
            }
            if ($scope.permission.student_module == true) {
                $scope.permission.student_module = 'true';
            } else {
                $scope.permission.student_module = 'false';
            }
            if ($scope.permission.master_module == true) {
                $scope.permission.master_module = 'true';
            } else {
                $scope.permission.master_module = 'false';
            }
            if ($scope.permission.fees_module == true) {
                $scope.permission.fees_module = 'true';
            } else {
                $scope.permission.fees_module = 'false';
            }
            if ($scope.permission.register_module == true) {
                $scope.permission.register_module = 'true';
            } else {
                $scope.permission.register_module = 'false';
            }
            if ($scope.permission.expense_module == true) {
                $scope.permission.expense_module = 'true';
            } else {
                $scope.permission.expense_module = 'false';
            }
            params = {
                'permission_details': angular.toJson($scope.permission),
                'csrfmiddlewaretoken': $scope.csrf_token,
            }
            $http({
                method:'post',
                url: '/staff/permissions/',
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                hide_spinner();
                document.location.href = '/staff/permissions/';
            }).error(function(data, status) {
                console.log('Request failed' || data);
            })
        }
    }
    $scope.new_staff = function() {
        $scope.staff = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password': '',
            'dob': '',
            'address': '',
            'mobile_number': '',
            'land_number': '',
            'email':'',
            'blood_group': '',
            'doj': '',
            'qualifications': '',
            'experience':'',
            'role': '',
        }
        var date_pick = new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#doj'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        $scope.staff_selected = false;
        $scope.new_staff = true;
        $scope.popup = new DialogueModelWindow({   
            'dialogue_popup_width': '79%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_staff_details'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.save_new_staff = function() {
        save_staff($scope, $http, 'permission');
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    } 
}