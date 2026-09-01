# 📚 KB Engebag

Sistema de **Base de Conhecimento (Knowledge Base)** para organização e consulta de artigos técnicos, com foco em usabilidade, agilidade na busca e organização da informação.

---

### Autor
* **Gabriel Malheiro** - [malheirovieira.g@gmail.com](mailto:malheirovieira.g@gmail.com)

## 🚀 Funcionalidades

- Portal De Acessos e Sistemas
- Redirecionamento WhatsApp
- Busca por título, categorias e tags  
- Navegação dinâmica com HTMX
- Cadastro de artigos
- Medidor de satisfação (NPS)
- Editor de texto com CKEditor  
- Interface simples e responsiva  

---

## 🛠️ Tecnologias

- Python  
- Django  
- HTML / CSS  
- JavaScript  
- HTMX  
- CKEditor  

---

## ⚙️ Como executar

```bash
git clone https://github.com/malheirovieira/kb_engebag.git
cd kb_engebag
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver (caso esteja em rede corporativa e queira rodar na rede inteira, acrescente no final do comando: 0.0.0.0:8000)
