from flask import Blueprint, request, jsonify
from .database import get_db_connection
from .models import Mahasiswa, MataKuliah

api = Blueprint('api', __name__)

# Mahasiswa Routes
@api.route('/mahasiswa', methods=['GET'])
def get_mahasiswa():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mahasiswa')
    mahasiswa_list = [Mahasiswa.from_db_row(row).__dict__ for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(mahasiswa_list)

@api.route('/mahasiswa/<int:id>', methods=['GET'])
def get_mahasiswa_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mahasiswa WHERE id = %s', (id,))
    mahasiswa = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if mahasiswa is None:
        return jsonify({'error': 'Mahasiswa not found'}), 404
    return jsonify(Mahasiswa.from_db_row(mahasiswa).__dict__)

@api.route('/mahasiswa', methods=['POST'])
def create_mahasiswa():
    data = request.get_json()
    required_fields = ['nim', 'nama', 'tanggal_lahir', 'alamat', 'jenis_kelamin']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mahasiswa (nim, nama, tanggal_lahir, alamat, jenis_kelamin) VALUES (%s, %s, %s, %s, %s)',
        (data['nim'], data['nama'], data['tanggal_lahir'], data['alamat'], data['jenis_kelamin'])
    )
    conn.commit()
    id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': id, 'message': 'Mahasiswa created successfully'}), 201

@api.route('/mahasiswa/<int:id>', methods=['PUT'])
def update_mahasiswa(id):
    data = request.get_json()
    fields = ['nim', 'nama', 'tanggal_lahir', 'alamat', 'jenis_kelamin']
    
    if not any(field in data for field in fields):
        return jsonify({'error': 'No fields to update'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    values = []
    for field in fields:
        if field in data:
            update_fields.append(f'{field} = %s')
            values.append(data[field])
    
    values.append(id)
    query = f"UPDATE mahasiswa SET {', '.join(update_fields)} WHERE id = %s"
    
    cursor.execute(query, values)
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected_rows == 0:
        return jsonify({'error': 'Mahasiswa not found'}), 404
    return jsonify({'message': 'Mahasiswa updated successfully'})

@api.route('/mahasiswa/<int:id>', methods=['DELETE'])
def delete_mahasiswa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mahasiswa WHERE id = %s', (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected_rows == 0:
        return jsonify({'error': 'Mahasiswa not found'}), 404
    return jsonify({'message': 'Mahasiswa deleted successfully'})

# Matakuliah Routes
@api.route('/matkul', methods=['GET'])
def get_matkul():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matkul')
    matkul_list = [MataKuliah.from_db_row(row).__dict__ for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(matkul_list)

@api.route('/matkul/<int:id>', methods=['GET'])
def get_matkul_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matkul WHERE id = %s', (id,))
    matkul = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if matkul is None:
        return jsonify({'error': 'Mata Kuliah not found'}), 404
    return jsonify(MataKuliah.from_db_row(matkul).__dict__)

@api.route('/matkul', methods=['POST'])
def create_matkul():
    data = request.get_json()
    required_fields = ['kode_mk', 'nama_mk', 'sks']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO matkul (kode_mk, nama_mk, sks) VALUES (%s, %s, %s)',
        (data['kode_mk'], data['nama_mk'], data['sks'])
    )
    conn.commit()
    id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': id, 'message': 'Mata Kuliah created successfully'}), 201

@api.route('/matkul/<int:id>', methods=['PUT'])
def update_matkul(id):
    data = request.get_json()
    fields = ['kode_mk', 'nama_mk', 'sks']
    
    if not any(field in data for field in fields):
        return jsonify({'error': 'No fields to update'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    values = []
    for field in fields:
        if field in data:
            update_fields.append(f'{field} = %s')
            values.append(data[field])
    
    values.append(id)
    query = f"UPDATE matkul SET {', '.join(update_fields)} WHERE id = %s"
    
    cursor.execute(query, values)
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected_rows == 0:
        return jsonify({'error': 'Mata Kuliah not found'}), 404
    return jsonify({'message': 'Mata Kuliah updated successfully'})

@api.route('/matkul/<int:id>', methods=['DELETE'])
def delete_matkul(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM matkul WHERE id = %s', (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    
    if affected_rows == 0:
        return jsonify({'error': 'Mata Kuliah not found'}), 404
    return jsonify({'message': 'Mata Kuliah deleted successfully'})