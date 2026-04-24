# 📚 KB Engebag

Sistema de **Base de Conhecimento (Knowledge Base)** para organização e consulta de artigos técnicos, com foco em usabilidade, agilidade na busca e organização da informação.

---

## 🚀 Funcionalidades

- Busca por título, categorias e tags  
- Navegação dinâmica com HTMX (sem recarregar a página)  
- Menu lateral hierárquico (categorias e subcategorias)  
- Cadastro de artigos com autor e data  
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
venv\Scripts\activate
pip install django
pip install django-ckeditor
python manage.py migrate
python manage.py runserver
