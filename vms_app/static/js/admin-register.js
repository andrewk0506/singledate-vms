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
        let err = "";
        let password = $("#input-password").val();
        let confirm = $("#input-confirm-password").val();

        if (("#new-staff-role-select").val() == "ADMIN") {
            if (!password) {
                err = "Password field cannot be empty";
            }
            else if (password  !== confirm) {
                err = "Password fields do not match";
            }
        }

        if (err) {
            event.preventDefault();
            $("#page-form-container").append(
                `
              <div class="alert alert-error alert-dismissible" role="alert">
                    <button type="button" class="close btn btn-danger" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    ${err}
              </div>
                `
            )
        }
    })