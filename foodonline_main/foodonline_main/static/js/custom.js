$(document).ready(function(){
    // Show correct quantities on page load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });

    // Handle Add to Cart
    $(document).on('click', '.add_to_cart', function(e){
    e.preventDefault();
    
    var food_id = $(this).attr('data-id');
    var url = $(this).attr('data-url');

    $.ajax({
        type: 'GET',
        url: url,
        data: {'food_id': food_id},
        success: function(response){
            if (response.status == 'login_required') {
            Swal.fire({
                icon: 'info',
                title: response.message,
                showConfirmButton: true,
                confirmButtonText: 'Login Now'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/login';
                }
            });
           }else if(response.status == 'failed'){
                swal.fire({
                    icon:'error',
                    title:response.message
                });
            }
             else{
                // Update the cart counter (top right)
                $('#cart_counter').html(response.cart_counter['cart_count']);
                 // ✅ Update the correct item quantity
                $('#qty-' + food_id).html(response.qty);
            }
                 }
             });
        });


        // Decrease the cart
        $(document).on('click','.decrease_cart',function(e){
            e.preventDefault();

            var food_id = $(this).attr('data-id');
            var url = $(this).attr('data-url');

            $.ajax({
                type:'GET',
                url :url,
                data:{
                    'food_id':food_id
                },
                success:function(response){
                   if (response.status == 'login_required') {
                        Swal.fire({
                            icon: 'info',
                            title: response.message,
                            showConfirmButton: true,
                            confirmButtonText: 'Login Now'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location.href = '/login';
                            }
                        });
                    }else if(response.status == 'failed'){
                            swal.fire({
                            icon:'error',
                            title:response.message
                                });
                    }else{
                         $('#cart_counter').html(response.cart_counter['cart_count']);
                         $('#qty-' + food_id).html(response.qty);
                        
                        }}
                        })
                    })
        

    // delete item from  cart
        $(document).on('click','.delete_item',function(e){
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
                        } else {
                            $('#cart_counter').html(response.cart_counter['cart_count']);
                            Swal.fire('Success', response.message, 'success');
                             $('#cart-item-' + food_id).remove();
                             
                           
                        }
                    }
                });
            });

            

});
