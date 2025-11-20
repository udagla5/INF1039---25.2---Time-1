/* static/js/ajax_bookmark.js */

document.addEventListener('DOMContentLoaded', () => {
    // Função para obter o token CSRF do cookie (necessário para requisições POST do Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.bookmark-col').forEach(col => {
        col.addEventListener('click', (event) => {
            // Encontra o item da oportunidade que contém o data-id
            const item = event.target.closest('[data-id]');
            if (!item) return;

            const oportunidadeId = item.getAttribute('data-id');

            // Preparação da requisição AJAX para a view do Django
            fetch('/toggle-favorito/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken // Token de segurança do Django
                },
                // Envia o ID da oportunidade no corpo
                body: `oportunidade_id=${oportunidadeId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Atualiza o visual com base na resposta do servidor
                    if (data.is_saved) {
                        item.classList.add('saved'); // Bandeirinha preenchida
                    } else {
                        item.classList.remove('saved'); // Bandeirinha vazia
                        
                        // Se estiver na página de Histórico e removeu, elimina do DOM
                        if (document.body.classList.contains('historico-page')) {
                            item.remove();
                        }
                    }
                } else {
                    console.error("Erro ao salvar/remover:", data.message);
                    alert("Erro: Não foi possível salvar a oportunidade.");
                }
            })
            .catch(error => {
                console.error('Erro na requisição AJAX:', error);
                alert("Ocorreu um erro de comunicação com o servidor.");
            });
        });
    });
});