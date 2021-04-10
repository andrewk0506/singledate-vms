    $("#add-admin-password").hide();
    $("#add-admin-confirm-password").hide();
    console.log("Jquery locked and loded!");
    $("#new-staff-role-select").on('change', function() {
        if (this.value === "ADMIN"){
            $("#add-admin-password").show();
            $("#add-admin-confirm-password").show();
        } else {
            $("#add-admin-password").hide();
            $("#add-admin-confirm-password").hide();
        }
    })

    $("#form-register-staff").submit(function(event) {
        alert("Handler for submit event called!");
        let err = "";
        let password = $("#input-password").val();
        let confirm = $("#input-confirm-password").val();

        alert("In submit handler");
        if (("#new-staff-role-select").val() == "ADMIN") {
            if (!password) {
                err = "Password field cannot be empty";
                alert(err);
            }
            else if (password  !== confirm) {
                err = "Password fields do not match";
                alert(err);
            }
        }

        alert("error is: ", err);
        if (err) {
            event.preventDefault();
            $("#error-messages").append(
                `<p class="error-message"> ${err} </p>`
            )
        }
    })