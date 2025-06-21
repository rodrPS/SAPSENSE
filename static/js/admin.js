function abrirModal(id) {
    document.getElementById('erroModal').innerText = '';
    document.getElementById('modalRegister').style.display = 'flex';

    const observer = new MutationObserver(() => {
    const texto = erroModal.innerText.trim();
    erroModal.style.display = texto ? 'flex' : 'none';
    });

    observer.observe(erroModal, { childList: true, subtree: true });
}

function fecharModal() {
    document.getElementById('modalRegister').style.display = 'none';
}

function saveUser() {
    const formElement = document.querySelector('#modalRegister form');
    const formData = new FormData(formElement);

    const nome = formData.get('nome');
    if (!nome.trim().includes(' ')) {
      document.getElementById('erroModal').innerText = 'Informe nome e sobrenome.';
      return;
    }

    fetch('/admin', {
      method: 'POST',
      body: formData
    }).then(res => {
      if (!res.ok) return res.json().then(data => { throw data.message });
      location.reload();
    }).catch(err => {
      document.getElementById('erroModal').innerText = err || 'Erro ao criar usuário.';
    });
}
