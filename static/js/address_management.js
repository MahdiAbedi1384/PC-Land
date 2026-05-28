// static/js/address_management.js

$(document).ready(function () {
    // Event delegation for dynamic content
    const $addressesList = $('#addresses-list');
    const $addressModalFormContainer = $('#address-modal-form-container');
    const $addressModal = $('#addressModal');
    const $addressModalLabel = $('#addressModalLabel');

    // Function to load the address form into the modal
    window.loadAddressForm = function (userId, addressId = null) {
        let url = `/accounts/addresses/form/${userId}/`;
        if (addressId) {
            url = `/accounts/addresses/form/${userId}/${addressId}/`;
            $addressModalLabel.text("ویرایش آدرس");
        } else {
            $addressModalLabel.text("افزودن آدرس جدید");
        }

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json', // Expecting JSON response
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            },
            success: function (data) {
                if (data.form_html) {
                    $addressModalFormContainer.html(data.form_html);
                    // Initialize Bootstrap components if needed (e.g., selectpicker, datepicker)
                    // Example: Initialize province/city dropdowns if they are not automatically handled
                    initializeAddressFormInteractions();
                } else {
                    $addressModalFormContainer.html('<p>خطا در بارگذاری فرم.</p>');
                }
            },
            error: function (error) {
                console.error("Error loading address form:", error);
                $addressModalFormContainer.html('<p>خطا در بارگذاری فرم. لطفاً دوباره امتحان کنید.</p>');
            }
        });
    };

    // Function to handle form submission (add/edit address)
    // Using event delegation on the modal form container
    $addressModalFormContainer.on('submit', '#address-form', function (event) {
        event.preventDefault(); // Prevent default form submission
        const $form = $(this);
        const url = $form.attr('action');
        const method = $form.attr('method');
        const formData = new FormData(this);

        $.ajax({
            url: url,
            type: method,
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            },
            success: function (data) {
                if (data.success) {
                    $addressModal.modal('hide');
                    // Reload the addresses list
                    loadAddresses();
                    // Optionally show a success message
                    showToast("آدرس با موفقیت ذخیره شد.");
                } else if (data.form_html) {
                    // Display validation errors
                    $addressModalFormContainer.html(data.form_html);
                    initializeAddressFormInteractions(); // Re-initialize after form replacement
                } else {
                    showToast("خطا در ذخیره آدرس. لطفاً دوباره امتحان کنید.", "error");
                }
            },
            error: function (error) {
                console.error("Error submitting address form:", error);
                showToast("خطا در ارتباط با سرور. لطفاً دوباره امتحان کنید.", "error");
            }
        });
    });

    // Function to load addresses list
    window.loadAddresses = function () {
        $.ajax({
            url: '/accounts/addresses/', // URL for listing addresses
            type: 'GET',
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            },
            success: function (data) {
                if (data.addresses_html) {
                    $('#addresses-list').html(data.addresses_html);
                    // Re-initialize any necessary JS for newly loaded elements if any
                    // Example: re-apply hover effects or button listeners if needed
                } else {
                    $('#addresses-list').html('<p>خطا در بارگذاری آدرس‌ها.</p>');
                }
            },
            error: function (error) {
                console.error("Error loading addresses:", error);
                $('#addresses-list').html('<p>خطا در بارگذاری آدرس‌ها.</p>');
            }
        });
    };

    // Function to delete an address
    window.deleteAddress = function (addressId) {
        $.ajax({
            url: `/accounts/addresses/${addressId}/delete/`, // URL for deleting address
            type: 'POST', // Usually POST for delete actions
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                // CSRF token for Django
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function (data) {
                if (data.success) {
                    showToast("آدرس با موفقیت حذف شد.");
                    loadAddresses(); // Refresh the list
                } else {
                    showToast("خطا در حذف آدرس. لطفاً دوباره امتحان کنید.", "error");
                }
            },
            error: function (error) {
                console.error("Error deleting address:", error);
                showToast("خطا در حذف آدرس. لطفاً دوباره امتحان کنید.", "error");
            }
        });
    };

    // Function to initialize interactions within the address form (e.g., province/city dropdown)
    function initializeAddressFormInteractions() {
        const $province = $("#id_province");
        const $city = $("#id_city");
        const $cityContainer = $("#city-field-container");

        const isUpdate = $("#address-form").data("is-update") === "true";
        const initialCityValue = $city.attr("data-initial") || "";

        function hideCityContainer() {
            $cityContainer.hide();
            $city.empty();
        }

        function showCityContainer() {
            $cityContainer.show();
        }

        hideCityContainer();

        $province.on("change", function () {
            const provinceId = $(this).val();

            if (!provinceId) {
                hideCityContainer();
                return;
            }

            $.ajax({
                url: `cities/${provinceId}/`,
                method: "GET",
                success: function (data) {
                    $city.empty();

                    data.cities.forEach(function (city) {
                        const option = $("<option>")
                            .val(city.id)
                            .text(city.name);
                        $city.append(option);
                    });

                    showCityContainer();

                    if (initialCityValue) {
                        $city.val(initialCityValue);
                    }
                }
            });
        });

        if (isUpdate && $province.val()) {
            $province.trigger("change");
        }
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Helper function for simple toast notifications
    function showToast(message, type = "success") {
        const toastContainer = $('#toast-container');
        if (toastContainer.length === 0) {
            $('body').append('<div id="toast-container" style="position: fixed; top: 20px; right: 20px; z-index: 1050;"></div>');
        }

        const toastId = `toast-${Date.now()}`;
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        $('#toast-container').prepend(toastHtml);

        const $toast = $(`#${toastId}`);
        $toast.toast('show');

        // Clean up toast element after it's hidden
        $toast.on('hidden.bs.toast', function () {
            $(this).remove();
        });
    }

    // Initial load of addresses when the page document is ready
    // loadAddresses(); // Uncomment if you want to load addresses on page load without user interaction

    // Click listener for the "Add Your First Address" button in the empty state
    $addressesList.on('click', '#open-add-address-modal-empty', function () {
        $('#open-add-address-modal').trigger('click'); // Trigger the main modal opener
    });
});
