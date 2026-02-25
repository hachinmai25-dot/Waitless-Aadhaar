from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQL
from utils.geo_allocator import find_nearest_center
import uuid, random
from datetime import datetime, timedelta

applicant_bp = Blueprint('applicant', __name__)

def get_mysql():
    from app import mysql
    return mysql

@applicant_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    
    cur.execute("""
        INSERT INTO applicants 
        (full_name, dob, gender, mobile, email, address, pincode, latitude, longitude, document_type, application_type)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['full_name'], data['dob'], data['gender'],
        data['mobile'], data.get('email'), data['address'],
        data['pincode'], data.get('latitude'), data.get('longitude'),
        data.get('document_type'), data.get('application_type', 'New')
    ))
    mysql.connection.commit()
    applicant_id = cur.lastrowid
    cur.close()

    return jsonify({"message": "Registered successfully", "applicant_id": applicant_id}), 201


@applicant_bp.route('/nearest-centers', methods=['POST'])
def nearest_centers():
    data = request.json
    lat = float(data['latitude'])
    lon = float(data['longitude'])
    
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM biometric_centers WHERE is_active = TRUE")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    centers = [dict(zip(cols, row)) for row in rows]
    cur.close()

    nearest = find_nearest_center(lat, lon, centers)
    return jsonify({"centers": nearest})


@applicant_bp.route('/book-slot', methods=['POST'])
def book_slot():
    data = request.json
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    # Generate token
    token = f"WLA-{random.randint(1000,9999)}"
    
    # Book appointment
    cur.execute("""
        INSERT INTO appointments (applicant_id, center_id, slot_date, slot_time, token_number)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['applicant_id'], data['center_id'],
          data['slot_date'], data['slot_time'], token))
    
    # Update center load
    cur.execute("UPDATE biometric_centers SET current_load = current_load + 1 WHERE id = %s",
                (data['center_id'],))
    
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Slot booked!", "token": token}), 201


@applicant_bp.route('/status/<mobile>', methods=['GET'])
def check_status(mobile):
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT a.full_name, a.status, ap.slot_date, ap.slot_time, ap.token_number, bc.name as center_name
        FROM applicants a
        LEFT JOIN appointments ap ON a.id = ap.applicant_id
        LEFT JOIN biometric_centers bc ON ap.center_id = bc.id
        WHERE a.mobile = %s
    """, (mobile,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    cols = [d[0] for d in cur.description]
    return jsonify(dict(zip(cols, row)))
