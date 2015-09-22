function loginFormController($scope, $http) {
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
    $scope.submit = function () {
        $http.post('/login');
    };
    $scope.checkname = function () {
        if ($scope.LoginFormData.login.length > 0) {
            $http.post('/checkname', "login=" + $scope.LoginFormData.login);
        }
    };
}