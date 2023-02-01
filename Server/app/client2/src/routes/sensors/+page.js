import api from '$lib/api';
export const trailingSlash = 'always';

export async function load() {
	try {
		const { devices } = await api.get('/devices');
		return { sensors: devices };
	} catch (error) {
		console.log(error);
		return { sensors: [] };
	}
}
