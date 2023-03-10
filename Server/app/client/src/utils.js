export async function fetchPOST(url, data) {
    const req = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return await req.json();
  }

  export async function fetchGET(url) {
    const req = await fetch(url, {
      method: 'GET'
    });
    return await req.json();
  }