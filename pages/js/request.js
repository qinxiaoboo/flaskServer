const BASE_URL = '/api';

const request = {
  req(method, url, body){
      if (method === "GET"){
          return fetch(`http://${server_address}:${server_port}${url}`,{
            method: method,
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "token": localStorage.getItem("token"),
                "groups": localStorage.getItem("groups")
            }
        })
      }
    return fetch(`http://${server_address}:${server_port}${url}`,{
            method: method,
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "token": localStorage.getItem("token"),
                "groups": localStorage.getItem("groups")
            },
            body: JSON.stringify(body)
        })

  },
  get(url){
    return this.req('GET',url, {});
  },
  post(url, payload){
    return this.req('POST',url, payload);
  },
  put(url, payload){
    return this.req('PUT',url, payload);
  },
  delete(url, payload){
    return this.req('DELETE',url, payload);
  },
}

