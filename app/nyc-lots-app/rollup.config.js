import { spawn } from 'child_process';
import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import json from '@rollup/plugin-json';
import livereload from 'rollup-plugin-livereload';
import terser from '@rollup/plugin-terser';
import css from 'rollup-plugin-css-only';


const production = !process.env.ROLLUP_WATCH;

function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		
		svelte({
			compilerOptions: {
				dev: !production
			}
		}),
		json(),
		css({ output: 'bundle.css' }),
		resolve({
			browser: true,
			dedupe: ['svelte'],
			exportConditions: ['svelte']
		}),
		commonjs(),

		// Serve static files from `static` folder
		!production &&
			serve({
				contentBase: ['public', 'static'], // Add 'static' here
				port: 5000,
			}),

		!production &&
			livereload({
				watch: 'public',
				// Include `static` directory for live-reloading
				verbose: true,
				contentBase: ['public', 'static']
			}),

		production && terser()
	],
	watch: {
		clearScreen: false
	}
};
