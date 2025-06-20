import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection

noticias_bp = Blueprint('noticias', __name__)

@noticias_bp.route('/')
def home():
    try:
        conn = get_db_connection()
        noticias = conn.execute("SELECT * FROM noticias").fetchall()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        noticias = []

    return render_template('home.html', noticias=noticias)

@noticias_bp.route('/agregar_noticia', methods=['GET', 'POST'])
def agregar_noticia():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        fecha = request.form['fecha']
        imagen = request.files['imagen']

        if imagen:
            imagen_path = os.path.join('static', 'imagenes_de_noticias', imagen.filename)
            imagen.save(imagen_path)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO noticias (titulo, contenido, fecha, imagen) VALUES (?, ?, ?, ?)",
                (titulo, contenido, fecha, imagen.filename)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al insertar: {e}")

        return redirect('/noticias')

    return render_template('agregar_noticia.html')

@noticias_bp.route('/noticias')
def ver_noticias():
    try:
        conn = get_db_connection()
        noticias = conn.execute("SELECT * FROM noticias ORDER BY id DESC").fetchall()
        conn.close()

        noticias_modificadas = []
        for noticia in noticias:
            contenido_corto = noticia['contenido'][:200] + "..." if len(noticia['contenido']) > 200 else noticia['contenido']
            noticias_modificadas.append({
                **noticia,
                'contenido': contenido_corto
            })

    except Exception as e:
        print(f"Error al obtener noticias: {e}")
        noticias_modificadas = []

    return render_template('noticias.html', noticias=noticias_modificadas)

@noticias_bp.route('/noticias/<int:noticia_id>')
def ver_noticia(noticia_id):
    try:
        conn = get_db_connection()
        noticia = conn.execute("SELECT * FROM noticias WHERE id = ?", (noticia_id,)).fetchone()
        conn.close()
        if noticia is None:
            flash('La noticia solicitada no existe.')
            return redirect(url_for('noticias.ver_noticias'))
    except Exception as e:
        print(f"Error: {e}")
        flash('Error al obtener la noticia.')
        return redirect(url_for('noticias.ver_noticias'))

    return render_template('noticia.html', noticia=noticia)
