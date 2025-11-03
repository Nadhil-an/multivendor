let autocomplete;

function initAutocomplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    { types: ['geocode', 'establishment'], componentRestrictions: { country: ['in'] } }
  );
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  const place = autocomplete.getPlace()
  console.log(place);
  document.getElementById('id_address').addEventListener('input',function(){
    console.log('Typed',this.value);
  })
  if (!place.geometry) {
    document.getElementById('id_address').placeholder = "Start typing...";
    return;
  }

  // Get latitude and longitude directly from the selected place
  const latitude = place.geometry.location.lat();
  const longitude = place.geometry.location.lng();

  // Fill your Django form fields
$('#id_latitude').val(latitude.toFixed(6));
$('#id_longitude').val(longitude.toFixed(6));

if (place.name) {
        $('#id_address').val(place.name);
    }


for (var i = 0; i < place.address_components.length; i++) {
    for (var j = 0; j < place.address_components[i].types.length; j++) {
        if (place.address_components[i].types[j] === 'country') {
            $('#id_country').val(place.address_components[i].long_name);
        } else if (place.address_components[i].types[j] === 'administrative_area_level_1') {
            $('#id_state').val(place.address_components[i].long_name);
        } else if (place.address_components[i].types[j] === 'locality') {
            $('#id_city').val(place.address_components[i].long_name);
        }else if(place.address_components[i].types[j] === 'postal_code'){
            $('#id_pin_code').val(place.address_components[i].long_name);
        }
    }
}

  console.log('Place selected:', place);
}





$(document).ready(function(){

    // ✅ Show correct quantities on page load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });

    // ✅ Add to Cart
    $(document).on('click', '.add_to_cart', function(e){
        e.preventDefault();

        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            data: {'food_id': food_id},
            success: function(response){
                if (response.status === 'login_required') {
                    Swal.fire({
                        icon: 'info',
                        title: response.message,
                        showConfirmButton: true,
                        confirmButtonText: 'Login Now'
                    }).then((result) => {
                        if (result.isConfirmed) window.location.href = '/login';
                    });
                }
                else if (response.status === 'failed') {
                    Swal.fire({
                        icon:'error',
                        title:response.message
                    });
                }
                else {
                    // ✅ Update cart counter and item quantity
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);
                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        });
    });

    // ✅ Decrease Cart Quantity
    $(document).on('click', '.decrease_cart', function(e){
        e.preventDefault();

        var food_id = $(this).attr('data-id');        // FoodItem ID
        var cart_id = $(this).attr('data-cart-id');   // Cart Item ID
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            data: {'food_id': food_id},
            success: function(response){
                if (response.status === 'login_required') {
                    Swal.fire({
                        icon: 'info',
                        title: response.message,
                        showConfirmButton: true,
                        confirmButtonText: 'Login Now'
                    }).then((result) => {
                        if (result.isConfirmed) window.location.href = '/login';
                    });
                }
                else if (response.status === 'failed') {
                    Swal.fire({
                        icon:'error',
                        title:response.message
                    });
                }
                else {
                    // ✅ Update cart counter and item quantity
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);
                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    // ✅ If quantity becomes 0, remove the li element
                    if (parseInt(response.qty) <= 0){
                        $('#cart-item-' + cart_id).fadeOut(300, function(){
                            $(this).remove();
                            displayEmptyText(); // check if cart is empty
                        });
                    }
                }
            }
        });
    });

    //  Delete Item from Cart
    $(document).on('click', '.delete_item', function(e){
        e.preventDefault();

        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url: url,
            success:function(response){
                if(response.status === 'failed'){
                    Swal.fire({
                        icon:'error',
                        title:response.message
                    });
                } 
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    Swal.fire('Success', response.message, 'success');
                    $('#cart-item-' + food_id).fadeOut(300, function(){
                        $(this).remove();
                        displayEmptyText();
                    });
                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        });
    });

    //  Check if Cart is Empty
    function displayEmptyText(){
        var cart_counter = parseInt($('#cart_counter').html());
        if(cart_counter === 0){
            $('#check-cart').show();
        }
    }

    function applyamount(subtotal,tax,grand_total){
        if (window.location.pathname = '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#grand_total').html(grand_total)
        }
    }

    //add hours
   $(document).on('click', '.add_hour', function(e) {
    e.preventDefault();

    var dayValue = $('#id_day').val();
    var dayText = $('#id_day option:selected').text(); // ✅ human-readable day
    var from_hour = $('#id_from_hour').val();
    var to_hour = $('#id_to_hour').val();
    var is_closed = $('#id_is_closed').is(':checked');
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    var url = $(this).attr('data-url');

    if (is_closed) {
        is_closed = 'True';
        if (dayValue === '') {
            Swal.fire({title: 'Please select a day', icon: 'info'});
            return;
        }
    } else {
        is_closed = 'False';
        if (dayValue === '' || from_hour === '' || to_hour === '') {
            Swal.fire({title: 'Please fill the input', icon: 'info'});
            return;
        }
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'day': dayValue,
            'from_hour': from_hour,
            'to_hour': to_hour,
            'is_closed': is_closed,
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function(response) {
            if (response.status === 'success') {
                let html = '';

                if (response.is_closed) {
                    html = `<tr><td><b>${response.day}</b></td><td>Closed</td><td><a href="#">Remove</a></td></tr>`;
                } else {
                    html = `<tr><td><b>${response.day}</b></td><td>${response.from_hour} - ${response.to_hour}</td><td><a href="#">Remove</a></td></tr>`;
                }

                $('.opening_hours').append(html);
                $('#opening_hours')[0].reset();
                Swal.fire({ title: 'Added successfully!', icon: 'success', timer: 1000, showConfirmButton: false });
            } else {
                Swal.fire(response.message, '', 'error');
            }
        }
    });
});


    

});
