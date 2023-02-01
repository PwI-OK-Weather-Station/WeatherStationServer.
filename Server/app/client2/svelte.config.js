import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({strict: false,
			pages: 'build',
			assets: 'build', 
			fallback: "index.html"}),
		prerender: { entries: [] }
	}
};

export default config;
