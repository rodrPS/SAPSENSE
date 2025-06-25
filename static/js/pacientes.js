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

function abrirModalPaciente(internacaoId) {
  fetch(`/pacientes/${internacaoId}/atualizar`)
    .then(res => res.text())
    .then(html => {
      document.getElementById("modalPacienteContainer").innerHTML = html;
      document.getElementById("modalPaciente").style.display = "flex";
      aplicarEventosModal(internacaoId); // <- Aplica os eventos separadamente
    });
}

function aplicarEventosModal(internacaoId) {
  setTimeout(() => {
    // Campos readonly
    document.querySelectorAll('input[name="reinternacao"]').forEach(radio => {
      radio.disabled = true;
    });

    // Submit AJAX
    const form = document.querySelector('#modalPaciente form');

    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              fecharModal();
              location.reload();
            } else if (data.html) {
              document.getElementById("modalPacienteContainer").innerHTML = data.html;
              aplicarEventosModal(internacaoId); // reativa os eventos no novo conteúdo
            } else if (data.error) {
              alert("Erro: " + data.error);
            }
          })
          .catch(error => {
            console.error("Erro:", error);
            alert("Erro ao enviar os dados.");
          });
      });
    }
  }, 100);
}

function fecharModal() {
  document.getElementById("modalPaciente").style.display = "none";
}
