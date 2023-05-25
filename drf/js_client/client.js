
const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const baseEndpoint = "http://localhost:8000/api"

if (loginForm){
    loginForm.addEventListener('submit',handleLogin)
}

if (searchForm){
    searchForm.addEventListener('submit',handleSearch)
}

function handleLogin(event){
    event.preventDefault()
    const LoginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodySTR = JSON.stringify(loginObjectData)
    const option = {
       method:'POST',
       headers:{
        'Content-Type':'application/json'
       },
       body:bodySTR
    }
    fetch(LoginEndpoint,option)
    .then(response=>{
        return response.json()
    })
    .then(authData=>{
        handleAuthData(authData,getProductList)
    })
    .catch(err=>{
        console.log('err',err)
    })
}

function handleSearch(event){ // First way of handling search
    event.preventDefault()
    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/?${searchParams}`
    const headers = {
        'Content-Type':'application/json',
    }
    const authToken = localStorage.getItem('access')
    if (authToken){
        headers['Authorization'] = `Bearer ${authToken}`
    }
    const option = {
       method:'GET',
       headers:headers
    }
    fetch(endpoint,option)
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        const validData = isTokenValid(data)
        if (validData && contentContainer){
            contentContainer.innerHTML = ""
            if (data && data.hits) {
                let htmlStr  = ""
                for (let result of data.hits) {
                    htmlStr += "<li>"+ result.title + "</li>"
                }
                contentContainer.innerHTML = htmlStr
                if (data.hits.length === 0) {
                    contentContainer.innerHTML = "<p>No results found</p>"
                }
            } 
            else {
                contentContainer.innerHTML = "<p>No results found</p>"
            }
        }
    })
    .catch(err=>{
        console.log('err',err)
    })
}

function handleAuthData(authData,callback){
    localStorage.setItem('access',authData.access)
    localStorage.setItem('refresh',authData.refresh)
    if (callback){
        callback()
    }
}

function writeToContainer(data){
    if (contentContainer){
        contentContainer.innerHTML = '<pre>'+ JSON.stringify(data,null,4) +'</pre>'
    }
}

function getFetchOption(method,body){
    return {
        method: method == null ?'GET' :method,
        headers:{
            'Content-Type': 'application/json',
            'Authorization':`Bearer ${localStorage.getItem('access')}`
        },
        body : body ?body : null
    }
}

function isTokenValid(jsonData){
    if(jsonData.code==='token_not_valid'){
        alert('Please Login again')
        return false
    }
    return true
}

function validateJWTToken() {
    // fetch
    const endpoint = `${baseEndpoint}/token/verify/`
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    }
    fetch(endpoint, options)
    .then(response=>response.json())
    .then(x=> {
        // refresh token
    })
}

function getProductList(){
    const endpoint = `${baseEndpoint}/products/`
    const option = getFetchOption()
    fetch(endpoint,option)
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        const validData = isTokenValid(data)
        if (validData){
            writeToContainer(data)
        }
    })
}

// validateJWTToken()

const searchClient = algoliasearch('Your Algo Username', 'Your Algo Api'); // second way of handling search

const search = instantsearch({
  indexName: 'cfe_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  instantsearch.widgets.clearRefinements({
    container: '#clear-refinement',
    attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
    container: '#user-list',
    attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
    container: '#public-list',
    attribute: 'public'
  }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
        item:` 
        <div>
            <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
            <div>{{#helpers.highlight}}{ "attribute": "body" }{{/helpers.highlight}}</div>
            <p>{{user}}</p><p>\${{price}}</p>
        </div>`
    }
  })
]);

search.start();
