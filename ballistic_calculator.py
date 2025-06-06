# Ballistic calculator with simple interface and SQLite database
import sqlite3
import math
import argparse

DB_FILE = 'ballistics.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ammo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bullet_weight REAL,
        ballistic_coefficient REAL,
        muzzle_velocity REAL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS weapons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        caliber TEXT,
        ammo_id INTEGER,
        FOREIGN KEY(ammo_id) REFERENCES ammo(id)
    )''')
    conn.commit()
    conn.close()


def add_ammo(name, weight, bc, velocity):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO ammo(name, bullet_weight, ballistic_coefficient, muzzle_velocity) VALUES (?, ?, ?, ?)',
                (name, weight, bc, velocity))
    conn.commit()
    conn.close()


def add_weapon(name, caliber, ammo_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO weapons(name, caliber, ammo_id) VALUES (?, ?, ?)', (name, caliber, ammo_id))
    conn.commit()
    conn.close()


def list_ammo():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT id, name, bullet_weight, ballistic_coefficient, muzzle_velocity FROM ammo')
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        print(f"ID: {row[0]} Name: {row[1]} Weight: {row[2]}g BC: {row[3]} Velocity: {row[4]} m/s")


def list_weapons():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''SELECT w.id, w.name, w.caliber, a.name FROM weapons w LEFT JOIN ammo a on w.ammo_id=a.id''')
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        print(f"ID: {row[0]} Name: {row[1]} Caliber: {row[2]} Ammo: {row[3]}")


def compute_trajectory(distance, angle_deg, velocity):
    angle_rad = math.radians(angle_deg)
    g = 9.81
    time = distance / (velocity * math.cos(angle_rad))
    drop = velocity * math.sin(angle_rad) * time - 0.5 * g * time ** 2
    return drop, time


def main():
    parser = argparse.ArgumentParser(description='Ballistic Calculator')
    subparsers = parser.add_subparsers(dest='command')

    init_parser = subparsers.add_parser('initdb', help='Initialize database')

    add_ammo_parser = subparsers.add_parser('add-ammo', help='Add ammunition')
    add_ammo_parser.add_argument('name')
    add_ammo_parser.add_argument('weight', type=float)
    add_ammo_parser.add_argument('bc', type=float)
    add_ammo_parser.add_argument('velocity', type=float)

    add_weapon_parser = subparsers.add_parser('add-weapon', help='Add weapon')
    add_weapon_parser.add_argument('name')
    add_weapon_parser.add_argument('caliber')
    add_weapon_parser.add_argument('ammo_id', type=int)

    list_ammo_parser = subparsers.add_parser('list-ammo', help='List ammunition')
    list_weapon_parser = subparsers.add_parser('list-weapons', help='List weapons')

    calc_parser = subparsers.add_parser('calc', help='Compute trajectory')
    calc_parser.add_argument('distance', type=float, help='Target distance (meters)')
    calc_parser.add_argument('angle', type=float, help='Shooting angle (degrees)')
    calc_parser.add_argument('velocity', type=float, help='Muzzle velocity (m/s)')

    args = parser.parse_args()

    if args.command == 'initdb':
        init_db()
        print('Database initialized.')
    elif args.command == 'add-ammo':
        add_ammo(args.name, args.weight, args.bc, args.velocity)
        print('Ammo added.')
    elif args.command == 'add-weapon':
        add_weapon(args.name, args.caliber, args.ammo_id)
        print('Weapon added.')
    elif args.command == 'list-ammo':
        list_ammo()
    elif args.command == 'list-weapons':
        list_weapons()
    elif args.command == 'calc':
        drop, time = compute_trajectory(args.distance, args.angle, args.velocity)
        print(f"Bullet drop: {drop:.2f} meters")
        print(f"Time of flight: {time:.2f} seconds")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
