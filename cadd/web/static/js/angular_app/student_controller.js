

function add_new_student($http, $scope){  

    $scope.hide_popup_windows();
    $('#add_student_details')[0].setStyle('display', 'block');        
    $scope.popup = new DialogueModelWindow({

        'dialogue_popup_width': '79%',
        'message_padding': '0px',
        'left': '28%',
        'top': '182px',
        'height': 'auto',
        'content_div': '#add_student_details'
    });
    // var height = $(document).height();
    // $scope.popup.set_overlay_height(height);
    $scope.popup.show_content();
}

function save_new_student($http, $scope) {
    if(validate_new_student($scope)) {
        $scope.dob = $$('#dob')[0].get('value');
        $scope.doj = $$('#doj')[0].get('value');
        for (var i=0; i<$scope.installments.length; i++) {
            id_name = '#'+$scope.installments[i].due_date_id;
            $scope.installments[i].due_date = $$(id_name)[0].get('value');
        }
        params = { 
            'enquiry': $scope.enquiry,
            'student_name':$scope.student_name,
            'roll_number': $scope.roll_number,
            'cadd_registration_no' : $scope.cadd_registration_no,
            'course': $scope.course,
            'batch': $scope.batch,        
            'qualifications': $scope.qualifications,
            'dob': $scope.dob,
            'address': $scope.address,
            'mobile_number': $scope.mobile_number,
            'email':$scope.email,
            'blood_group': $scope.blood_group,
            'doj': $scope.doj,
            'intial_payment': $scope.intial_payment,
            'certificates_submitted': $scope.certificates_submitted,
            'id_proofs_submitted': $scope.id_proof,
            'guardian_name': $scope.guardian_name,
            'relationship': $scope.relationship,
            'guardian_mobile_number': $scope.guardian_mobile_number,
            'fees': $scope.fees_after_discount,
            'discount': $scope.discount,
            'installments': angular.toJson($scope.installments),
            'no_installments': $scope.no_installments,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        var fd = new FormData();
        fd.append('photo_img', $scope.photo_img.src)
        for(var key in params){
            fd.append(key, params[key]);          
        }
        var url = "/admission/add_student/";
        $http.post(url, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined
            }
        }).success(function(data, status){
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            } else {
                
                document.location.href ="/admission/student_admission/";
            }
        }).error(function(data, status){
            $scope.error_flag=true;
            $scope.validation_error = data.message;
            $('#spinner').css('height', '0px');
        });
    }
}

function reset_student($scope) {

    $scope.student_name = '';
    $scope.roll_number = '';
    $scope.cadd_registration_no = '';
    $scope.course = '';
    $scope.batch = '';
    $scope.semester = '';
    $scope.qualifications = '';
    $scope.dob = '';
    $scope.address = '';
    $scope.mobile_number = '';
    $scope.email = '';
    $scope.blood_group = '';
    $scope.doj = '';
    $scope.intial_payment = 0;
    $scope.certificates_submitted = '';
    $scope.id_proof = '';
    $scope.guardian_name = '';
    $scope.relationship = '';
    $scope.photo_img = {};
}
validate_new_student = function($scope) {
    $scope.validation_error = '';
    $scope.dob = $$('#dob')[0].get('value');
    $scope.doj = $$('#doj')[0].get('value');
    var total = 0;

    for (var i=0; i<$scope.installments.length; i++) {
        if ($scope.installments[i].amount == Number($scope.installments[i].amount)) {
            total = parseFloat(total) + parseFloat($scope.installments[i].amount)
        }
    }
    if($scope.student_name == '' || $scope.student_name == undefined) {
        $scope.validation_error = "Please Enter the Name" ;
        return false;
    } else if($scope.roll_number == '' || $scope.roll_number == undefined) {
        $scope.validation_error = "Please Enter the Roll Number" ;
        return false;
    } else if($scope.course == '' || $scope.course == undefined) {
        $scope.validation_error = "Please Enter Course";
        return false;
    } else if($scope.batch == '' || $scope.batch == undefined) {
        $scope.validation_error = "Please Enter Batch";
        return false;
    } else if($scope.dob == '' || $scope.dob == undefined) {
        $scope.validation_error = "Please Enter DOB";
        return false;
    } else if($scope.address == '' || $scope.address == undefined) {
        $scope.validation_error = "Please Enter Address";
        return false;
    } else if($scope.mobile_number == ''|| $scope.mobile_number == undefined){
        $scope.validation_error = "Please enter the Mobile Number";
        return false;
    } else if($scope.mobile_number.length < 9 || $scope.mobile_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Mobile Number";
        return false;
    } else if(($scope.email != '' && $scope.email != undefined) && (!(validateEmail($scope.email)))){
        $scope.validation_error = "Please enter a Valid Email Id";
        return false;
    } else if($scope.blood_group == '' || $scope.blood_group == undefined) {
        $scope.validation_error = "Please Enter Blood Group";
        return false; 
    } else if($scope.doj == '' || $scope.doj == undefined) {
        $scope.validation_error = "Please Enter Date of Join";
        return false;
    }else if($scope.certificates_submitted == '' || $scope.certificates_submitted == undefined) {
        $scope.validation_error = "Please enter certificates submitted";
        return false;
    } else if($scope.id_proof == '' || $scope.id_proof == undefined) {
         $scope.validation_error = "Please enter id proofs submitted";
        return false; 
    } else if($scope.guardian_name == '' || $scope.guardian_name == undefined) {
        $scope.validation_error = "Please Enter the Guardian Name" ;
        return false;
    }  else if($scope.relationship == '' || $scope.relationship == undefined) {
        $scope.validation_error = "Please Enter Relationship";
        return false;
    } else if($scope.guardian_mobile_number == ''|| $scope.guardian_mobile_number == undefined){
        $scope.validation_error = "Please enter the Guardian Mobile Number";
        return false;
    } else if($scope.guardian_mobile_number.length < 9 || $scope.guardian_mobile_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Mobile Number";
        return false;
    } else if ($scope.fees == '' || $scope.fees == undefined) {
        $scope.validation_error = "Please enter fees";
        return false;
    } else if ($scope.no_installments == '' || $scope.no_installments == undefined) {
        $scope.validation_error = "Please enter no of installments";
        return false;
    } else if ($scope.fees_after_discount != total) {
        $scope.validation_error = 'Please check the installment amount with the total';
        return false;
    } else if ($scope.installments.length > 0) {
        for(var i = 0; i < $scope.installments.length; i++){
            id_name = '#'+$scope.installments[i].due_date_id;
            $scope.installments[i].due_date = $$(id_name)[0].get('value');
            var date_value = $scope.installments[i].due_date.split('/');
            var start_date = new Date(date_value[2],date_value[1]-1, date_value[0]); 
            $scope.installments[i].due_date = $$(id_name)[0].get('value');
            if($scope.installments[i].amount == ''){
                $scope.validation_error = "Please enter the amount for installment";
                return false;
            } else if($scope.installments[i].amount && !Number($scope.installments[i].amount)){
                $scope.validation_error = "Please enter a valid amount for installment";
                return false;
            } else if($scope.installments[i].due_date == ''){
                $scope.validation_error = "Please enter the due date for installment";
                return false;
            } //else if($scope.installments[i].fine != 0 && parseFloat($scope.installments[i].fine) != Number($scope.installments[i].fine)){
            //     $scope.validation_error = "Please enter a valid fine amount for installment";
            //     return false;
            // } 
            for(var j = i+1; j < $scope.installments.length; j++){
                id_name = '#'+$scope.installments[j].due_date_id;
                $scope.installments[j].due_date = $$(id_name)[0].get('value');
                var date_value = $scope.installments[j].due_date.split('/');
                var next_date = new Date(date_value[2],date_value[1]-1, date_value[0]);
                if(start_date > next_date){
                    $scope.validation_error = "Please check the due date in row " + (j+1);
                    return false;
                }
            }
        }
    } return true;
}   
function EditStudentController($scope, $http, $element, $location, $timeout) {

    $scope.init = function(csrf_token, student_id){
        $scope.csrf_token = csrf_token;
        $scope.student_id = student_id;
        $scope.get_student_details(student_id);
        $scope.student = {
            'student_name': '',
            'roll_number': '',
            'course': '',
            'batch': [],
            'qualifications': '',            
            'dob': '',
            'address': '',
            'mobile_number': '',
            'email': '',
            'blood_group': '',            
            'doj': '',
            'cadd_registration_no': '',
            'id_proofs_submitted': '',
            'guardian_name': '',
            'relationship': '',
            'guardian_mobile_number': '',            
            'fees': '',
            'fees_after_discount': '',
            'discount': 0,
            'no_installments': '',
        }
        $scope.photo_img = {};
        $scope.url = '/admission/edit_student_details/' + $scope.student_id+ '/';
        new Picker.Date($$('#dob'), {
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
        
        get_course_list($scope, $http);
        get_batches($scope, $http, 'edit_student');
        
    }
    $scope.get_fees = function() {
        for(var i=0; i<$scope.courses.length; i++) {
            if ($scope.student.course == $scope.courses[i].id) {
                $scope.student.fees = $scope.courses[i].amount;
            }
        }
    }
    $scope.calculate_actual_fees = function(){
        $scope.student.fees_after_discount = parseFloat($scope.student.fees) -  parseFloat($scope.student.discount) - parseFloat($scope.student.intial_payment);
    }
    $scope.get_student_details  = function(student_id){
        $scope.url = '/admission/edit_student_details/' + student_id+ '/';
        $http.get($scope.url).success(function(data)
        {
            $scope.student = data.student[0];
            $scope.student.batch = [];
            $scope.no_installments = data.student[0].no_installments;
            $scope.installments = $scope.student.installments;
            for(var i = 0; i < $scope.student.batches.length; i++){
                $scope.student.batch.push($scope.student.batches[i].id);
            }
            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.load_installments = function() {
        if ($scope.student.no_installments.length > 0) {
            if ($scope.student.no_installments > $scope.installments.length) {
                diff = $scope.student.no_installments - $scope.installments.length;
                for (var i=0; i<diff; i++) {
                    due_date_id = 'due_date_'+$scope.installments.length;
                    $scope.installments.push({
                        'amount': '',
                        'fine': '',
                        'due_date': '',
                        'due_date_id': due_date_id,
                    })
                }
            } else {
                diff = $scope.installments.length - $scope.student.no_installments;
                for (var i=diff; i>0; i--) {
                    index = $scope.installments.indexOf($scope.installments[$scope.installments.length])
                    $scope.installments.splice(index, 1);
                }
            }   
        }
    }
    $scope.attach_date_picker = function(installment) {
        id_name = '#' +installment.due_date_id;
        new Picker.Date($$(id_name), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.validate_edit_student = function() {
        $scope.validation_error = '';
        $scope.student.dob = $$('#dob')[0].get('value');
        $scope.student.doj = $$('#doj')[0].get('value');
        var total = 0;
        for (var i=0; i<$scope.installments.length; i++) {
            if ($scope.installments[i].amount == Number($scope.installments[i].amount)) {
                total = parseFloat(total) + parseFloat($scope.installments[i].amount)
            }
        }
        console.log(total);
        if($scope.student.student_name == '' || $scope.student.student_name == undefined) {
            $scope.validation_error = "Please Enter the Name" ;
            return false;
        } else if($scope.student.roll_number == '' || $scope.student.roll_number == undefined) {
            $scope.validation_error = "Please Enter the Roll Number" ;
            return false;
        } else if($scope.student.course == '' || $scope.student.course == undefined) {
            $scope.validation_error = "Please Enter Course";
            return false;
        } else if($scope.student.batch == '' || $scope.student.batch == undefined) {
            $scope.validation_error = "Please Enter Batch";
            return false;
        } else if($scope.student.dob == '' || $scope.student.dob == undefined) {
            $scope.validation_error = "Please Enter DOB";
            return false;
        } else if($scope.student.address == '' || $scope.student.address == undefined) {
            $scope.validation_error = "Please Enter Address";
            return false;
        } else if($scope.student.mobile_number == ''|| $scope.student.mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if($scope.student.mobile_number.length < 9 || $scope.student.mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if(!(validateEmail($scope.student.email))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;
        } else if($scope.student.blood_group == '' || $scope.student.blood_group == undefined) {
            $scope.validation_error = "Please Enter Blood Group";
            return false; 
        } else if($scope.student.doj == '' || $scope.student.doj == undefined) {
            $scope.validation_error = "Please Enter Date of Join";
            return false;
        } else if($scope.student.certificates_submitted == '' || $scope.student.certificates_submitted == undefined) {
            $scope.validation_error = "Please enter certificates submitted";
            return false;
        } else if($scope.student.id_proofs_submitted == '' || $scope.student.id_proofs_submitted == undefined) {
             $scope.validation_error = "Please enter id proofs submitted";
            return false; 
        } else if($scope.student.guardian_name == '' || $scope.student.guardian_name == undefined) {
            $scope.validation_error = "Please Enter the Guardian Name" ;
            return false;
        }  else if($scope.student.relationship == '' || $scope.student.relationship == undefined) {
            $scope.validation_error = "Please Enter Relationship";
            return false;
        } else if($scope.student.guardian_mobile_number == ''|| $scope.student.guardian_mobile_number == undefined){
            $scope.validation_error = "Please enter the Guardian Mobile Number";
            return false;
        } else if($scope.student.guardian_mobile_number.length < 9 || $scope.student.guardian_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if ($scope.student.fees == '' || $scope.student.fees == undefined) {
            $scope.validation_error = "Please enter fees";
            return false;
        } else if ($scope.student.no_installments == '' || $scope.student.no_installments == undefined) {
            $scope.validation_error = "Please enter no of installments";
            return false;
        } else if ($scope.student.fees_after_discount != total) {
            $scope.validation_error = 'Please check the installment amount with the total';
            return false;
        }  else if ($scope.student.fees_after_discount > $scope.student.fees) {
            $scope.validation_error = 'Please check the fees with actual fees';
            return false;
        }else if ($scope.installments.length > 0) {
            for(var i = 0; i < $scope.installments.length; i++){
                id_name = '#'+$scope.installments[i].due_date_id;
                $scope.installments[i].due_date = $$(id_name)[0].get('value');
                var date_value = $scope.installments[i].due_date.split('/');
                var start_date = new Date(date_value[2],date_value[1]-1, date_value[0]);                
                if($scope.installments[i].amount == ''){
                    $scope.validation_error = "Please enter the amount for installment in row " + (i+1);
                    return false;
                } else if($scope.installments[i].amount && !Number($scope.installments[i].amount)){
                    $scope.validation_error = "Please enter a valid amount for installment in row " + (i+1);
                    return false;
                } else if($scope.installments[i].due_date == ''){
                    $scope.validation_error = "Please enter the due date for installment in row " + (i+1);
                    return false;
                } else if($scope.installments[i].fine != 0 && parseFloat($scope.installments[i].fine) != Number($scope.installments[i].fine)){
                    $scope.validation_error = "Please enter a valid fine amount for installment in row " + (i+1);
                    return false;
                } 
                for(var j = i+1; j < $scope.installments.length; j++){
                    id_name = '#'+$scope.installments[j].due_date_id;
                    $scope.installments[j].due_date = $$(id_name)[0].get('value');
                    var date_value = $scope.installments[j].due_date.split('/');
                    var next_date = new Date(date_value[2],date_value[1]-1, date_value[0]);
                    if(start_date > next_date){
                        $scope.validation_error = "Please check the due date in row " + (j+1);
                        return false;
                    }
                }
            }
        } return true;
    }   
    $scope.save_student = function() {
        if ($scope.validate_edit_student()){
            $scope.error_flag=false;
            $scope.message = '';
            $scope.url = '/admission/edit_student_details/' + $scope.student.student_id+ '/';
            params = { 
                'student': angular.toJson($scope.student),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            var fd = new FormData();
            fd.append('photo_img', $scope.photo_img.src)
            for(var key in params){
                fd.append(key, params[key]);          
            }
            $http.post($scope.url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/admission/list_student/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function StudentListController($scope, $http, $element, $location, $timeout) {

    $scope.init = function(csrf_token,student_id){
        get_batches($scope, $http);
        $scope.page_interval = 10;
        $scope.visible_list = [];
        $scope.students = [];
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';      
        $scope.pages = 1;
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
        reset_student($scope);
    }
    
    $scope.get_students = function(){
        var url = '/admission/list_student/?batch_id='+ $scope.batch;
        $http.get(url).success(function(data)
        {
            $scope.students = data.students;
            paginate(data.students, $scope);
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    
    
    $scope.edit_student_details = function(student){
        $scope.student_id = student.id;
        document.location.href = '/admission/edit_student_details/'+ $scope.student_id+ '/';
    } 
    
    $scope.display_student_details = function(student) {
        $scope.student_id = student.id;
        $scope.url = '/admission/view_student_details/' + $scope.student_id+ '/';
        $http.get($scope.url).success(function(data)
        {
            $scope.student = data.student[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });


        $('#student_details_view')[0].setStyle('display', 'block');
        
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#student_details_view'
        });
        
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.select_page = function(page){
        select_page(page, $scope.students, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}
function EnquiryController($scope, $http) {

    $scope.enquiry = {
        'mode': '',
        'student_name' : '',
        'address' :'',
        'mobile_number' : '',
        'email' : '',
        'details_about_clients_enquiry' : '',
        'educational_qualification' : '',
        'land_mark' : '',
        'course' : '',
        'remarks': '',
        'fess': '',
        'discount' : 0,
        'date': '',
        'follow_up': [],
    }
    $scope.enquiry.follow_up.push({
        'follow_up_date' : '',
        'remarks_for_follow_up_date' : '',
        'hide_button': false,
        'follow_up_date_id': 0,
    })
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        get_course_list($scope, $http);
        new Picker.Date($$('#date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.add_follow_up = function(){
        var i = $scope.enquiry.follow_up.length;
        var enquiry = $scope.enquiry.follow_up[i-1];
        i = enquiry['follow_up_date_id'] ;
        $scope.enquiry.follow_up.push({
            'follow_up_date' : '',
            'remarks_for_follow_up_date' : '',
            'hide_button': false,
            'follow_up_date_id': i+1,
        })
    }
    $scope.get_fees = function() {
        console.log($scope.enquiry.course, $scope.courses);

        for(var i=0; i<$scope.courses.length; i++) {
            if ($scope.enquiry.course == $scope.courses[i].id) {
                $scope.enquiry.fees = $scope.courses[i].amount;
               
            }
        }
    }
    $scope.attach_date_picker = function(follow_up){
        var id_name = '#';
        id_name = id_name + follow_up.follow_up_date_id;
        new Picker.Date($$(id_name), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.remove_follow_up = function(follow_up){
        var follow_up_id = $scope.enquiry.follow_up.indexOf(follow_up);
        if($scope.enquiry.follow_up.length > 1){
            $scope.enquiry.follow_up.splice(follow_up_id, 1);
            var len = $scope.enquiry.follow_up.length;
            $scope.enquiry.follow_up[len-1].hide_button = false;
        }
    }
    $scope.validate_enquiry = function() {
        $scope.validation_error = '';
        for(var i = 0; i < $scope.enquiry.follow_up.length; i++){
            id = '#' + $scope.enquiry.follow_up[i].follow_up_date_id;
            $scope.enquiry.follow_up[i].follow_up_date = $$(id)[0].get('value');
        }
        $scope.enquiry.date = $$('#date')[0].get('value');
        if($scope.enquiry.student_name == '' || $scope.enquiry.student_name == undefined) {
            $scope.validation_error = "Please Enter the Name" ;
            return false;
        } else if($scope.enquiry.address == '' || $scope.enquiry.address == undefined) {
            $scope.validation_error = "Please Enter Address";
            return false;
        } else if($scope.enquiry.mobile_number == ''|| $scope.enquiry.mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.enquiry.mobile_number)) || $scope.enquiry.mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.enquiry.date == '' || $scope.enquiry.date == undefined) {
            $scope.validation_error = "Please Enter  date of enquiry";
            return false;
        } else if($scope.enquiry.course == '' || $scope.enquiry.course == undefined) {
            $scope.validation_error = "Please Enter Course";
            return false;
        } else if(($scope.enquiry.email != '' && $scope.enquiry.email != undefined) && (!(validateEmail($scope.enquiry.email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;
        } else if($scope.enquiry.discount && !Number($scope.enquiry.discount)) {
            $scope.validation_error = "Please Enter  a avalid amount for discount";
            return false;
        }else if($scope.enquiry.discount > $scope.enquiry.fees) {
            $scope.validation_error = "Please Check with the Fees Amount";
            return false;
        }
        for(var i = 0; i < $scope.enquiry.follow_up.length; i++){
            if($scope.enquiry.follow_up[i].follow_up_date == ''){
                $scope.validation_error = "Please Enter the follow up date";
                return false;
            }
            var date_value = $scope.enquiry.follow_up[i].follow_up_date.split('/');
            var start_date = new Date(date_value[2],date_value[1]-1, date_value[0]); 
            for(var j = i+1; j < $scope.enquiry.follow_up.length; j++){
                var date_value = $scope.enquiry.follow_up[j].follow_up_date.split('/');
                var next_date = new Date(date_value[2],date_value[1]-1, date_value[0]);
                if(start_date > next_date){
                    $scope.validation_error = "Please check the follow up dates";
                    return false;
                }
            }
        }
        return true;
    }   
    $scope.save_enquiry = function(){
        if ($scope.validate_enquiry()) {
            for(var i = 0; i < $scope.enquiry.follow_up.length; i++){
                if($scope.enquiry.follow_up[i].hide_button == true)
                    $scope.enquiry.follow_up[i].hide_button = 'true';
                else
                    $scope.enquiry.follow_up[i].hide_button = 'false';
            }
            params = {
                'enquiry': angular.toJson($scope.enquiry),
                'csrfmiddlewaretoken': $scope.csrf_token,
                }
            
            $http({
                method: 'post',
                url: '/admission/enquiry/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                if (data.result == 'ok') {
                    document.location.href = '/admission/enquiry/'    
                } 
            }).error(function(data, status){
                console.log('Request failed'||data);
            });
        }
    }
}
function AdmissionController($scope, $http) {

    $scope.show_enquiry_search =  false;
    $scope.admission_type = 'Admission';
    $scope.photo_img = {};
    $scope.installments = [];
    $scope.search = {
        'student_name': '',
        'enquiry_num': '',
    }
    $scope.student_name = '';
    $scope.roll_number = '';
    $scope.cadd_registration_no = '';
    $scope.course = '';
    $scope.batch = '';
    $scope.semester = '';
    $scope.qualifications = '';
    $scope.dob = '';
    $scope.address = '';
    $scope.no_installments = 0;
    $scope.mobile_number = '';
    $scope.email = '';
    $scope.blood_group = '';
    $scope.doj = '';
    $scope.intial_payment = 0;
    $scope.certificates_submitted = '';
    $scope.id_proof = '';
    $scope.guardian_name = '';
    $scope.relationship = '';
    $scope.photo_img = {};
    $scope.fees_after_discount = 0;
    $scope.discount = 0;
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.no_enquiries = false;
        get_course_list($scope, $http);
        get_batch_list($scope,$http);
        new Picker.Date($$('#dob'), {
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
    $scope.enquiry_search  = function() {    
        var url = '/admission/enquiry_search/?student_name='+$scope.search.student_name;
        $http.get(url).success(function(data)
        {
            $scope.enquiries = data.enquiries; 
            $scope.count = data.count;
            if($scope.count == 0){
                $scope.no_count_msg  = '';
                
            }else{
                $scope.no_count_msg = $scope.count+'enquiry(s) found.';
            }
            if(data.enquiries.length == 0){
                $scope.no_enquiry_msg = 'No Enquiries found for this Student.';
                
            } else{
                $scope.no_enquiry_msg = '';
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.change_admission_type = function(admission_type){
        if(admission_type=='Enquiry'){
            $scope.show_enquiry_search =  true;
        }else{
            $scope.show_enquiry_search =  false;
        }
    }
    $scope.get_enquiry_details = function(){

        var url = '/admission/enquiry_details/?enquiry_num='+$scope.enquiry_num;
        $http.get(url).success(function(data)
        {   
            $scope.no_enquiry_msg = '';
            $scope.no_enquiry_msg = '';
            $scope.enquiries = '';
            $scope.search.student_name = '';
            if (data.enquiry.length == 0)
                $scope.no_enquiry_msg = 'No such enquiry';
            else {
                $scope.no_count_msg  = '';
                $scope.student_name = data.enquiry[0].student_name;
                $scope.course = data.enquiry[0].course;
                $scope.address = data.enquiry[0].address;
                $scope.qualifications = data.enquiry[0].educational_qualification;
                $scope.email = data.enquiry[0].email;
                $scope.mobile_number = data.enquiry[0].mobile_number;
                $scope.enquiry = data.enquiry[0].id;
                $scope.discount = data.enquiry[0].discount;
                $scope.get_fees();
                
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.save_new_student = function(){
        save_new_student($http, $scope);
    }
    $scope.load_installments = function() {
        $scope.installments = [];
        $scope.doj = $$('#doj')[0].get('value');
        $scope.temp_installments = $scope.installments;
        if ($scope.no_installments.length > 0) {
            if ($scope.no_installments > $scope.installments.length) {
                diff = 0;
                diff = $scope.no_installments - $scope.installments.length;

                for (var i=0; i<diff; i++) {
                    due_date_id = 'due_date_'+$scope.installments.length;
                    amount = 0
                    var x,y,z
                    date = new Date();
                    var mydate = new Date($scope.doj);
                    x = mydate.getDay();
                    console.log(x)
                    y = date.getMonth() + i + 2;
                    console.log(y)
                   
                    if (y <= 12){
                        z = date.getFullYear();
                    }
                    else{
                        y = y - 12;
                        z = date.getFullYear() + 1;
                    }
                    console.log(y,z)
                    console.log($scope.fees_after_discount)
                    amount = $scope.fees_after_discount / $scope.no_installments ;
                    $scope.installments.push({
                        'amount': amount,
                        'fine': $scope.fine,
                        'due_date': x+ '/' + y + '/' +z,
                        'due_date_id': due_date_id,
                    })
                }
            } else {
                diff = $scope.installments.length - $scope.no_installments;
                for (var i=diff; i>0; i--) {
                    index = $scope.installments.indexOf($scope.installments[$scope.installments.length])
                    $scope.installments.splice(index, 1);
                }
            }
        } else {
            $scope.installments = $scope.temp_installments;
        }
    }
    $scope.attach_date_picker = function(installment) {
        id_name = '#' +installment.due_date_id;
        new Picker.Date($$(id_name), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.calculate_actual_fees = function(){
        $scope.fees_after_discount = parseFloat($scope.fees) - parseFloat($scope.discount)  - parseFloat($scope.intial_payment);
    }
    $scope.get_fees = function() {
        for(var i=0; i<$scope.courses.length; i++) {
            if ($scope.course == $scope.courses[i].id) {
                $scope.fees = $scope.courses[i].amount;
                $scope.calculate_actual_fees();
            }
        }
    }
}
function EnquiryReportController($scope, $http) {

    $scope.start_date = '';
    $scope.end_date = '';
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.validate = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if($scope.start_date == ''){
            $scope.validate_error_msg = 'Please select the start date';
            return false;
        } else if($scope.end_date == ''){
            $scope.validate_error_msg = 'Please select the end date';
            return false;
        } return true;
    }
    $scope.view_enquiry = function(){
        if($scope.validate()){
            $http.get('/admission/enquiry_report?start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                if(data.result=='ok'){
                    $scope.validate_error_msg =  '';
                    $scope.enquiries = data.enquiries;
                    paginate(data.enquiries, $scope);
                }else{
                    $scope.validate_error_msg = "No enquiries  found";
                }
            }).error(function(data, status){
                $scope.message = data.message;
            })
        }
    } 
    $scope.get_enquiry_report = function(){
        $scope.start_date= $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        document.location.href = '/admission/enquiry_report?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&report_type=pdf';
    } 
    $scope.select_page = function(page){
        select_page(page, $scope.enquiries, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    } 
}
function AdmissionReportController($scope, $http) {

    $scope.start_date = '';
    $scope.end_date = '';
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.validate = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if($scope.start_date == ''){
            $scope.validate_error_msg = 'Please select the start date';
            return false;
        } else if($scope.end_date == ''){
            $scope.validate_error_msg = 'Please select the end date';
            return false;
        } return true;
    }
    $scope.view_admission = function(){
        if($scope.validate()){
            $http.get('/admission/admission_report?start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                if(data.result=='ok'){
                    $scope.validate_error_msg = '';
                    $scope.admissions = data.admissions;
                    paginate(data.admissions, $scope);
                }else{
                    $scope.validate_error_msg = "No admissions  found";
                }
            }).error(function(data, status){
                $scope.message = data.message;
            })
        }
    } 
    $scope.get_admission_report = function(){
        $scope.start_date= $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        document.location.href = '/admission/admission_report?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&report_type=pdf';
    }
    $scope.select_page = function(page){
        select_page(page, $scope.admissions, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }  
}
function EnquiryListController($scope, $http) {

    $scope.start_date = '';
    $scope.end_date = '';
    $scope.init = function(csrf_token){
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        $scope.csrf_token = csrf_token;
        var url = '/admission/all_enquiries/';
        $http.get(url).success(function(data)
        {   
            $scope.no_enquiry_msg = '';
            if (data.enquiry.length == 0)
                $scope.no_enquiry_msg = 'No such enquiry';
            else {
               $scope.enquiries = data.enquiry;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.display_enquiry_details = function(enquiry) {
        $scope.enquiry_id = enquiry.id;
        $scope.url = '/admission/enquiry_details?enquiry_id='+$scope.enquiry_id;
        $http.get($scope.url).success(function(data)
        {
            $scope.enquiry = data.enquiry[0];
            paginate(data.enquiry, $scope);
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        $('#enquiry_details_view')[0].setStyle('display', 'block');
        
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#enquiry_details_view'
        });
        
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.select_page = function(page){
        select_page(page, $scope.enquiry, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.display_followup_details = function(enquiry) {
        $scope.followups = [];
        $scope.followups = enquiry.follow_ups;
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#followup_details_view'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    
}
function FollowUpReportController($scope, $http) {

    $scope.start_date = '';
    $scope.end_date = '';
    $scope.init = function(csrf_token){
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var url = '/admission/follow_up_details/';
        $http.get(url).success(function(data)
        {   
            $scope.no_enquiry_msg = '';
            if (data.enquiries.length == 0)
                $scope.no_enquiry_msg = 'No enquiry present today for follow up';
            else {
               $scope.enquiries = data.enquiries;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
    }
    $scope.display_followup_details = function(enquiry) {
        $scope.followups = [];
        $scope.followups = enquiry.follow_ups;
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#followup_details_view'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.view_follow_ups = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        $scope.url = '/admission/follow_up_details/?start_date='+$scope.start_date+'&end_date='+$scope.end_date;
        $http.get($scope.url).success(function(data)
        {
            $scope.no_enquiry_msg = '';
            if (data.enquiries.length == 0)
                $scope.no_enquiry_msg = 'No  enquiry';
            else {
               $scope.enquiries = data.enquiries;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.display_enquiry_details = function(enquiry) {
        $scope.enquiry_id = enquiry.id;
        $scope.url = '/admission/enquiry_details?enquiry_id='+$scope.enquiry_id;
        $http.get($scope.url).success(function(data)
        {
            $scope.enquiry = data.enquiry[0];
            paginate(data.enquiry, $scope);
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });

        $('#enquiry_details_view')[0].setStyle('display', 'block');
        
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#enquiry_details_view'
        });
        
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.select_page = function(page){
        select_page(page, $scope.enquiries, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}
function EnquiryToAdmissionController($scope, $http) {
    $scope.start_date = '';
    $scope.end_date = '';
    $scope.report_type = 'completed';
    $scope.init = function(csrf_token){
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.display_followup_details = function(enquiry) {
        $scope.followups = [];
        $scope.followups = enquiry.follow_ups;
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#followup_details_view'
        });
        // var height = $(document).height();
        // $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.view_enquiry_to_admission = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if($scope.validate()){
            if($scope.report_type == 'completed'){
                $scope.url = '/admission/enquiry_to_admission/?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&completed='+$scope.report_type;
            }else if($scope.report_type == 'incompleted'){
                $scope.url = '/admission/enquiry_to_admission/?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&incompleted='+$scope.report_type;

            }
            $http.get($scope.url).success(function(data)
            {
                $scope.no_enquiry_msg = '';
                if (data.enquiries.length == 0)
                    $scope.no_enquiry_msg = 'No  enquiry';
                else {
                   $scope.enquiries = data.enquiries;
                   paginate(data.enquiries, $scope);
                }
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
    }
    $scope.generate_report = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if($scope.validate()){
            if($scope.report_type == 'completed'){
                document.location.href = '/admission/enquiry_to_admission/?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&completed='+$scope.report_type;
            }else if($scope.report_type == 'incompleted'){
                document.location.href = '/admission/enquiry_to_admission/?start_date='+$scope.start_date+'&end_date='+$scope.end_date+'&incompleted='+$scope.report_type;

            }
        }
    }
    $scope.change_report_type = function(report_type){
        if(report_type == 'completed'){
            $scope.report_type = report_type;
        }else if(report_type == 'incompleted'){
            $scope.report_type = report_type;
        }
    }
    $scope.validate = function(){
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        $scope.no_enquiry_msg = '';
        if($scope.start_date == ''){
            $scope.no_enquiry_msg = 'Please select the start date';
            return false;
        } else if($scope.end_date == ''){
            $scope.no_enquiry_msg = 'Please select the end date';
            return false;
        } return true;
    }
    $scope.select_page = function(page){
        select_page(page, $scope.enquiries, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}
function AdmissionCardController($scope, $http, $element) {
    
   
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
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
    $scope.get_admission_card = function(){
        document.location.href = '/admission/admission_card/?student_id='+$scope.student_id;
    }
}