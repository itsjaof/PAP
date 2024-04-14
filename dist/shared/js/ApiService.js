function resolveForm(formName) {
    const form = document.querySelector(`#${formName}`);

	form.addEventListener('submit', async (event) => {
		event.preventDefault();
		event.stopPropagation();

		const formData = new FormData(form);
		const url = form.action

		try {
			const response = await fetch(url, {
				method: 'POST',
				body: formData
			})

			if (!response.ok) {
				return false;
			}

            return true;

		} catch(error) {
			console.error(`Error requesting the API: ${error}`)
		}
    })
}