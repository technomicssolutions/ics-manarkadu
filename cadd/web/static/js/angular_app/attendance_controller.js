function attendance_validation($scope, $http){
    $scope.validation_error = "";
    if($scope.students.length == 0){
        $scope.validation_error = 'No students in this batch ';
        return false;
    } else if($scope.batch.id == '') {
        $scope.validation_error = 'Please choose batch';
        return false;
    } else if($scope.batch.topics == '') {
        $scope.validation_error = 'Please enter the topics covered';
        return false;
    } return true;
}
function student_search($scope, $http){
    if ($scope.batch_id == undefined){
        $scope.batch_id = ''
    }
    $http.get('/admission/search_student/?name='+$scope.student_name+'&batch='+$scope.batch_id).success(function(data){
        if(data.result == 'ok'){
            $scope.students_list = data.students;
            if($scope.students_list.length == 0)
                $scope.no_student_msg = "No Students found";
        }            
        }).error(function(data, status){
            console.log('Request failed'|| data);
        });
}
function staff_search($scope, $http){
    $http.get('/staff/search_staff/?name='+$scope.staff_name).success(function(data){
            $scope.staffs_list = data.staffs;
            if($scope.staffs_list.length == 0)
                $scope.no_staff_msg = "No Staff found";
        }).error(function(data, status){
            console.log('Request failed'|| data);
        });
}
function AttendanceController($scope, $http, $element){
    $scope.batch_id = "";
    $scope.students = {}
    $scope.is_edit = false;   
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_batches($scope, $http);
        $scope.show_buttons = true;
        $scope.batch = {
            'id': '',
            'topics': '',
            'remarks': '',
        }
    }
    $scope.get_batch_details = function(batch){
        var url = '/attendance/batch_students/'+batch.id;
        $http.get(url).success(function(data)
        {
            $scope.students = data.students;
            $scope.current_month = data.current_month;
            $scope.current_year = data.current_year;
            $scope.current_date = data.current_date;
            $scope.batch.topics = data.topics;
            $scope.batch.remarks = data.remarks;
            $scope.batch.staff = data.staff;
            for(var i = 0; i < $scope.students.length; i++){
                if($scope.students[i].is_presented == 'true')
                    $scope.students[i].is_presented = true;
                else 
                    $scope.students[i].is_presented = false;
            }
            if($scope.students.length == 0)
                $scope.validation_error = "No students in this batch";
            else
                $scope.validation_error = "";
        }).error(function(data, status){

        });
    }
    $scope.appliedClass = function(day) {
        if (day.is_holiday == 'true'){
            return "red_color";
        } 
        else if(day.is_future_date == 'true') {
          return "blue_color";  
        }
    }

    $scope.edit_attendance = function() {
        $scope.is_edit = true;
    }   

    $scope.save_attendance = function() {
        if(attendance_validation($scope, $http)) {
           for(var i = 0; i < $scope.students.length; i++){
                if($scope.students[i].is_presented == true)
                    $scope.students[i].is_presented = 'true';
                else
                    $scope.students[i].is_presented = 'false';
           }
            params = { 
                'batch': angular.toJson($scope.batch),
                'students': angular.toJson($scope.students),
                'current_month': $scope.current_month,
                'current_year': $scope.current_year,
                'current_date': $scope.current_date,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method : 'post',
                url : '/attendance/add_attendance/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                document.location.href = '/attendance/add_attendance/';
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status){
                console.log('error - ', data);
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            });
        }
    }
}

function AttendanceDetailsController($scope, $element, $http) {

    $scope.year = [];
    $scope.batch_month = '';
    $scope.batch_year = '';
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.keyboard_control();
        get_batches($scope, $http);
        $scope.batch_id = '';
        $scope.monthly_attendance = false
        $scope.show_batch_select = false
        $scope.daily_attendance = false;
        $scope.show_buttons = false;
        $scope.show_data = false;
        $scope.batch = {
            'id': '',
            'staff': '',
            'remarks': '',
            'topics': '',
        }
        new Picker.Date($$('#attendance_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    var date = new Date();
    var current_year = date.getFullYear(); 
    var start_year = current_year - 4;
    current_year = current_year + 4;
    for(var i=start_year; i<=current_year; i++){
        $scope.year.push(i);
    }
    $scope.keyboard_control = function(){
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
    }
    $scope.select_list_item = function(index) {
        student = $scope.students_list[index];
        $scope.get_student_details(student);
    }
    $scope.attendance_validation = function() {
        $scope.validation_error = "";
        if($scope.attendance_view == "1" || $scope.attendance_view == undefined){
            if($scope.batch_id == '' || $scope.batch_id == undefined) {
                $scope.validation_error = 'Please choose the Batch';
                return false;
            } else if($scope.batch_month == '' || $scope.batch_month == undefined) {
                $scope.validation_error = 'Please choose the Month';
                return false;
            } else if($scope.batch_year == '' || $scope.batch_year == undefined) {
                $scope.validation_error = 'Please choose the Year';
                return false;
            } return true;
        }
        else if($scope.attendance_view == "2"){
            $scope.attendance_date = $$('#attendance_date')[0].get('value');
            if($scope.attendance_date == '' || $scope.attendance_date == undefined) {
                $scope.validation_error = 'Please choose the Date';
                return false;
            } return true;
        } else if($scope.attendance_view == "3"){
            $scope.attendance_list = "";
            $scope.student_name = "";
            $scope.students_list = [];
            return false;
        }

    }
    $scope.appliedClass = function(day) {
        if(day.is_future_date == 'true') {
          return "blue_color";  
        }
    }
    $scope.edit_attendance = function() {
        $scope.is_edit = true;
    }
    $scope.attendance_view_by = function(){
        $scope.validation_error = "";
        if($scope.attendance_view == "1"){            
            $scope.show_batch_select = true;
            $scope.monthly_attendance = true;
            $scope.daily_attendance = false;
            $scope.show_buttons = false;
            $scope.show_data = false;
            $scope.batch_id = "";
            $scope.student_attendance = false;
        }
        else if($scope.attendance_view == "2"){            
            $scope.show_batch_select = true;       
            $scope.daily_attendance = true;
            $scope.show_buttons = true;
            $scope.monthly_attendance = false;  
            $scope.show_data = false;         
            $scope.batch_id = "";
            $scope.student_attendance = false;
        } else if($scope.attendance_view == "3"){            
            $scope.show_batch_select = true;       
            $scope.daily_attendance = false;
            $scope.show_buttons = false;
            $scope.monthly_attendance = false;  
            $scope.show_data = false;         
            $scope.batch_id = "";
            $scope.student_attendance = true;
        } 
    }
    $scope.student_search = function(){
        if($scope.student_name.length > 0){
            $scope.validation_error = "";
            if($scope.batch_id != ''){
                student_search($scope, $http);
            }                
            else
                $scope.validation_error = "Please select a Batch";
        }
        else{
            $scope.students_list = "";
            $scope.attendance_list = "";
        }            
    }
    $scope.get_student_details = function(student) {
        $scope.student_name = student.name;
        $scope.students_list = [];
        $scope.no_student_msg = "";
        var url = '/attendance/job_card/?batch='+$scope.batch_id+'&student='+student.id;
        $http.get(url).success(function(data)
        {
            $scope.view = data.view;
            $scope.attendance_list = data.attendance_list;
            $scope.show_data = true;
            console.log($scope.attendance_list);
        }).error(function(data, status)
        {
            $('#overlay').css('height', '0px');
            $('#spinner').css('height', '0px');
            console.log(data || "Request failed");
        });
    }
    $scope.get_attendance_details = function() {
        if ($scope.attendance_validation()) {
            $scope.validation_error = "";
            var height = $(document).height();
            height = height + 'px';
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            $scope.validation_error = '';
            $scope.show_data = true;  
            if($scope.attendance_view == "1" || $scope.attendance_view == undefined){
                var url = '/attendance/attendance_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.batch_year+'&batch_month='+$scope.batch_month;                
            }
            else {
                $scope.attendance_date = $$('#attendance_date')[0].get('value');
                $scope.date_array = $scope.attendance_date.split('/')
                var url = '/attendance/attendance_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.date_array[2]+'&batch_month='+$scope.date_array[1]+'&batch_day='+$scope.date_array[0];
            }            
            
            $http.get(url).success(function(data)
            {
                $scope.view = data.view;
                if($scope.view == 'monthly'){
                    $scope.students = data.batch[0].students;
                    $scope.columns = data.batch[0].column_count;  
                } else if($scope.view == 'daily'){
                    $scope.students = data.students;
                    $scope.batch.topics = data.topics;
                    $scope.batch.remarks = data.remarks;
                    $scope.batch.staff = data.staff;
                    $scope.batch.id = data.batch_id;
                    if(data.is_future_date == "true")
                        $scope.show_buttons = false;
                    else
                        $scope.show_buttons = true;
                    for(var i = 0; i < $scope.students.length; i++){
                        if($scope.students[i].is_presented == 'true')
                            $scope.students[i].is_presented = true;
                        else 
                            $scope.students[i].is_presented = false;
                    }
                }

                if ($scope.students.length == 0){
                    $scope.show_buttons = false;
                    $scope.validation_error = 'No Students';
                }
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status)
            {
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
                console.log(data || "Request failed");
            });
        }
    }
    $scope.save_attendance = function() {
        if(attendance_validation($scope, $http)) {
            var height = $(document).height();
            height = height + 'px';
           
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            for (var i=0; i < $scope.students.length; i++){
                if($scope.students[i].is_presented == true)
                    $scope.students[i].is_presented = "true";
                else
                    $scope.students[i].is_presented = "false";
            }
            $scope.attendance_date = $$('#attendance_date')[0].get('value');
            $scope.date_array = $scope.attendance_date.split('/')
            params = { 
                'batch': angular.toJson($scope.batch),
                'students': angular.toJson($scope.students),             
                'current_date': $scope.date_array[0], 
                'current_month': $scope.date_array[1],  
                'current_year': $scope.date_array[2],   
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : '/attendance/add_attendance/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/attendance/attendance_details/';
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status){
                console.log('error - ', data);
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            });
        }
    }
    $scope.clear_batch_details = function() {
        $scope.attendance_view = 1;
        if ($scope.attendance_validation()) {
            $scope.popup = new DialogueModelWindow({
                
                'dialogue_popup_width': '20%',
                'message_padding': '0px',
                'left': '28%',
                'top': '182px',
                'height': 'auto',
                'content_div': '#clear_batch_details_message'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.clear_batch = function(){
        $scope.batch_id = '';
        $scope.show_data = false;
        $scope.show_buttons = false;
        $scope.is_edit = false;
    }
    $scope.clear_ok = function() {
        document.location.href = '/attendance/clear_batch_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.batch_year+'&batch_month='+$scope.batch_month;
    }
    $scope.clear_cancel = function() {
        $scope.popup.hide_popup();
    }
}

function JobCardController($scope, $http){
    $scope.init = function(){
        get_batches($scope, $http);
        $scope.batch_id = "";
        $scope.student_name = "";
        $scope.keyboard_control();
        $scope.job_card = {
            'batch_id': '',
            'student_id': '',
        };
    }
    $scope.keyboard_control = function(){
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
    }
    $scope.select_list_item = function(index) {
        student = $scope.students_list[index];
        $scope.get_student_details(student);
    }
    $scope.get_student_details = function(student) {
        $scope.student_name = student.name;
        $scope.job_card.student_id = student.id;
        $scope.students_list = [];
        $scope.no_student_msg = "";
    }
    $scope.student_search = function(){
        if($scope.student_name.length > 0){
            $scope.message = "";
            if($scope.batch_id != ''){
                $scope.job_card.student_id = "";
                student_search($scope, $http);
            }                
            else
                $scope.message = "Please select a Batch";
        }
        else
            $scope.students_list = ""
    }
    $scope.select_batch = function(){
        $scope.student_name = "";
        $scope.message = "";
        $scope.students_list = "";
        $scope.job_card = {
            'batch_id': $scope.batch_id,
            'student_id': '',
        };
    }
    $scope.validate_jobcard = function(){
        $scope.message = "";
        if($scope.job_card.batch_id == ''){
            $scope.message = "Please select a batch from the list";
            return false;
        } else if($scope.job_card.student_id == ''){
            $scope.message = "Please select a student form the list";
            return false;
        } return true;
    }
    $scope.show_jobcard = function(){
        if($scope.validate_jobcard()){
            document.location.href = '/attendance/job_card/?batch='+$scope.job_card.batch_id+'&student='+$scope.job_card.student_id;
        }
    }
}

function AttendanceReportController($scope, $http) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_batches($scope, $http);
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
        } else if ($scope.batch == '' || $scope.batch == undefined) {
            $scope.error_message = 'Please choose the batch';
        } else {
            document.location.href = '/attendance/attendance_report/?batch='+$scope.batch+'&start_date='+start_date+'&end_date='+end_date;
        }
    }
}

function TopicsController($scope, $http, $element){
    $scope.init = function(){
        $scope.keyboard_control()
    }
    $scope.staff_search = function(){
        $scope.no_staff_msg = "";
        if($scope.staff_name.length > 0){
            staff_search($scope, $http);
        }
        else{
            $scope.staffs_list = "";
            $scope.topics = "";
        }    
    }
    $scope.keyboard_control = function(){
        $scope.focusIndex = 0;
        $scope.keys = [];
        $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
        $scope.keys.push({ code: 38, action: function() { 
            if($scope.focusIndex > 0){
                $scope.focusIndex--; 
            }
        }});
        $scope.keys.push({ code: 40, action: function() { 
            if($scope.focusIndex < $scope.staffs_list.length-1){
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
    }
    $scope.select_list_item = function(index) {
        staff = $scope.staffs_list[index];
        $scope.get_staff_details(staff);
    }
    $scope.get_staff_details = function(staff) {
        $scope.staff_name = staff.name;
        $scope.staffs_list = [];
        $scope.no_staff_msg = "";
        var url = '/attendance/topics_covered/?staff='+staff.id;
        $http.get(url).success(function(data)
        {   if(data.topics == '')
                $scope.no_staff_msg = 'No topics covered by the staff selected';
            else        
                $scope.topics = data.topics;
        }).error(function(data, status)
        {
            $('#overlay').css('height', '0px');
            $('#spinner').css('height', '0px');
            console.log(data || "Request failed");
        });
    }
}