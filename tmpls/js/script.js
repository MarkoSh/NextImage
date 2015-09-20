function loginFormController($scope) {
    $scope.submit = function () {

    };
    $scope.checkname = function () {
        if ($scope.LoginFormData.login.length > 3) {
            console.warn($scope);
        }
    }
}