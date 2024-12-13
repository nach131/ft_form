const urlparams = new URLSearchParams(window.location.search);
let code = urlparams.get('code');
let state = urlparams.get('state');
if (code && state){
    const queryParams = new URLSearchParams({code , state}).toString();
    const url = `http://localhost:8000/login/handleCallback?${queryParams}`;
    fetch(url , {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.access && data.refresh_token){
            document.cookie = `access_token=${data.access_token}`;
            document.cookie = `refresh_token=${data.refresh_token}`;
            localStorage.setItem('username', data.username);

            localStorage.setItem('user_img', data.user_img);
            localStorage.setItem('is_staff', data.is_staff);
            localStorage.setItem('coalition', data.coalition);22
            localStorage.setItem('color', data.color);
            localStorage.setItem('coalition_img', data.coalition_img);
            localStorage.setItem('title', data.title);
            localStorage.setItem('id', data.id);

            // color, coalicion, coalicion_img, title

            if (data.is_staff === 'true'){
                window.location.href = 'http://localhost:8000/staffHome';
            }else{
                window.location.href = 'http://localhost:8000/studentHome';
            }
        }else{
            console.log('Error: Failed to obtain access-tokens', data);
            console.log('Access-token:', data.access_token);
            window.location.href = 'http://localhost:8000/';
        }
    })
    .catch(error => {
        console.log('Error: failed token exchange', error);
        console.log('Access-token:', data.access_token);
    });
}else{
    console.log('Error: Missing code or state');
    console.log('Access-token:', data.access_token);
}
