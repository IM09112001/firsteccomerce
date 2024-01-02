let updateBtns = document.body.querySelectorAll('.update-cart')
for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
    let productId = this.dataset.product
    let action = this.dataset.action

    console.log('USER:', user);
    if (user === 'AnonymousUser') {
        addCookieItem(productId, action)
    }
    else{
        updateUserOrder(productId, action)
    }
})}

function addCookieItem(productId, action){
    console.log('Not logged in');

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= undefined) {
            console.log('Item shoutld be deleted');
            delete cart[productId]
        }
    } 
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...');
    
    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((responce) => {
        return responce.json();
    })
    .then(data=>{
        console.log('data:', data);
        location.reload(url)
    })
}

