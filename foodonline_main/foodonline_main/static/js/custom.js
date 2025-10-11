$(document).ready(function(){
    $(document).on('click', '.add_to_cart', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url')

        data ={
            food_id:food_id,
        }

        $.ajax({
            type :'GET',
            url : url,
            data:data,
            success:function(response){
               console.log(response);
            }
        })

    })
})

