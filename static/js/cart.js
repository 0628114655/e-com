var updateBtn = document.getElementsByClassName('update-item')
for (i = 0; i < updateBtn.length; i++)
{
    updateBtn[i].addEventListener('click', function (){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:' , productId, 'action:', action)
        console.log('user:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }
        else{
            updatUserOrder(productId, action)
        }
    })
}
function addCookieItem(productId, action) {
    console.log('Not logged in..');
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } 
        else {
            cart[productId]['quantity'] += 1;
        }
    }
    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;
        
        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }
    console.log('cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}

function updatUserOrder(productId,action){ 
        console.log('User is logged in, sending data..')
        var url = '/update_items/'
        fetch (url, {
            method : 'POST',
            headers : {
                'content-type' : 'application/json',
                'X-CSRFToken' : csrftoken,
            },
            body : JSON.stringify({'productId' : productId, 'action' : action})
        })
        .then((Response) => {
            return Response.json()
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
    }




