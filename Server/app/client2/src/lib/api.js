class API {
	constructor() {
		this.url = 'http://127.0.0.1:5000/api';
	}

	async get(path) {
		const res = await fetch(`${this.url}${path}`, {
			credentials: "include"
		  });
		return res.json();
	}

	async post(path, data = {}) {
		const res = await fetch(`${this.url}${path}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(data),
			credentials: "include"
		});
		return res.json();
	}
}

export default new API();
