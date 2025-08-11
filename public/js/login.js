document.addEventListener('DOMContentLoaded', () => {
	const root = document.querySelector('.logForm');
	if (!root) {
		console.error('[login.js] Container .logForm not found');
		return;
	}

	// Helpers
	const el = (tag, props = {}, children = []) => {
		const node = document.createElement(tag);
		Object.entries(props).forEach(([k, v]) => {
			if (k === 'text') node.textContent = v;
			else if (k === 'html') node.innerHTML = v;
			else if (k in node) node[k] = v;
			else node.setAttribute(k, v);
		});
		[].concat(children).filter(Boolean).forEach(c => node.appendChild(c));
		return node;
	};

	const labeledInput = ({ id, label, type = 'text', name, placeholder = '', required = true, autocomplete }) => {
		const input = el('input', { id, name, type, placeholder });
		if (required) input.required = true;
		if (autocomplete) input.autocomplete = autocomplete;
		const lab = el('label', { htmlFor: id, text: label });
		const wrap = el('div', {}, [lab, input]);
		return { wrap, input };
	};

	// Title
	const title = el('h1', { text: 'Byte Duel' });
	const subtitle = el('h2', { text: 'Connexion / Inscription' });

	// Tabs (simple buttons, no CSS)
	const tabs = el('div');
	const btnLogin = el('button', { type: 'button', text: 'Connexion' });
	const btnRegister = el('button', { type: 'button', text: 'Inscription' });
	tabs.appendChild(btnLogin);
	tabs.appendChild(btnRegister);

	// Status messages
	const status = el('div', { role: 'status', id: 'status' });

	// Login form
	const loginForm = el('form', { id: 'loginForm', noValidate: true });
	const loginEmail = labeledInput({ id: 'loginEmail', label: 'Email', type: 'email', name: 'email', placeholder: 'votre@email', autocomplete: 'email' });
	const loginPassword = labeledInput({ id: 'loginPassword', label: 'Mot de passe', type: 'password', name: 'password', placeholder: '••••••••', autocomplete: 'current-password' });
	const loginSubmit = el('button', { type: 'submit', text: 'Se connecter' });
	loginForm.append(loginEmail.wrap, loginPassword.wrap, loginSubmit);

	// Register form
	const registerForm = el('form', { id: 'registerForm', noValidate: true });
	const regUsername = labeledInput({ id: 'regUsername', label: 'Pseudo', type: 'text', name: 'username', placeholder: 'Votre pseudo', autocomplete: 'username' });
	const regEmail = labeledInput({ id: 'regEmail', label: 'Email', type: 'email', name: 'email', placeholder: 'votre@email', autocomplete: 'email' });
	const regPassword = labeledInput({ id: 'regPassword', label: 'Mot de passe', type: 'password', name: 'password', placeholder: '••••••••', autocomplete: 'new-password' });
	const regPassword2 = labeledInput({ id: 'regPassword2', label: 'Confirmez le mot de passe', type: 'password', name: 'password2', placeholder: '••••••••', autocomplete: 'new-password' });
	const registerSubmit = el('button', { type: 'submit', text: "S'inscrire" });
	registerForm.append(regUsername.wrap, regEmail.wrap, regPassword.wrap, regPassword2.wrap, registerSubmit);

	// Visibility toggle
	const showForm = (which) => {
		if (which === 'login') {
			loginForm.hidden = false;
			registerForm.hidden = true;
			status.textContent = '';
		} else {
			loginForm.hidden = true;
			registerForm.hidden = false;
			status.textContent = '';
		}
	};
	btnLogin.addEventListener('click', () => showForm('login'));
	btnRegister.addEventListener('click', () => showForm('register'));

			// Config: allow overriding API base via window.BYTE_DUEL_API
			// If running from file:// or capacitor://, fallback to localhost:8000
			const computedOrigin = (location.origin && /^https?:/i.test(location.origin)) ? location.origin : 'http://localhost:8000';
			const API_BASE = (window.BYTE_DUEL_API || computedOrigin).replace(/\/$/, '');

		// Helpers
		const postJSON = async (path, body) => {
			const res = await fetch(`${API_BASE}${path}`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(body),
			});
			const json = await res.json().catch(() => ({}));
			if (!res.ok || json.ok === false) {
				const msg = json?.detail || json?.error || `HTTP ${res.status}`;
				throw new Error(msg);
			}
			return json;
		};

		// Handlers
		loginForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			status.textContent = 'Connexion en cours...';
			try {
				const data = Object.fromEntries(new FormData(loginForm).entries());
				const payload = data.email
					? { email: data.email, password: data.password }
					: { username: data.username, password: data.password };
				const res = await postJSON('/auth/login', payload);
				if (res.key) {
					localStorage.setItem('auth_key', res.key);
				}
				status.textContent = 'Connecté ! Redirection...';
				// Redirect to menu
				window.location.href = '/pages/menu.html';
			} catch (err) {
				status.textContent = `Erreur: ${err.message}`;
			}
		});

		registerForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			const data = Object.fromEntries(new FormData(registerForm).entries());
			if (!data.password || data.password !== data.password2) {
				status.textContent = 'Les mots de passe ne correspondent pas.';
				return;
			}
			status.textContent = "Inscription en cours...";
			try {
				const res = await postJSON('/auth/register', {
					username: data.username,
					email: data.email,
					password: data.password,
				});
				if (res.key) {
					localStorage.setItem('auth_key', res.key);
				}
				status.textContent = 'Compte créé ! Redirection...';
				window.location.href = '/pages/menu.html';
			} catch (err) {
				status.textContent = `Erreur: ${err.message}`;
			}
		});

	// Compose UI
	root.append(title, subtitle, tabs, status, loginForm, registerForm);
	// Default view
	showForm('login');
});


