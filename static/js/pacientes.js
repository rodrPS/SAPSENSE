function abrirModal(id) {
  document.getElementById('internacaoId').value = id;
  document.getElementById('nomeResponsavel').value = '';
  document.getElementById('erroModal').innerText = '';
  document.getElementById('modalResponsavel').style.display = 'flex';
}

function fecharModal() {
  document.getElementById('modalResponsavel').style.display = 'none';
}

function salvarResponsavel() {
  const nome = document.getElementById('nomeResponsavel').value;
  const id = document.getElementById('internacaoId').value;

  if (!nome.trim().includes(' ')) {
    document.getElementById('erroModal').innerText = 'Informe nome e sobrenome.';
    return;
  }

  fetch('/atribuir-responsavel', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: id, responsavel: nome})
  }).then(res => {
    if (!res.ok) return res.json().then(data => { throw data.message });
    location.reload();
  }).catch(err => {
    document.getElementById('erroModal').innerText = err || 'Erro ao salvar.';
  });
}
