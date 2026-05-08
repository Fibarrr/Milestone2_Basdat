"""
Cara pakai:
    pip install faker
    python seed.py > seed_data.sql
    python seed.py --klan 250 --akun 5000 --seed 42 > seed_data.sql
    mysql -u root -p clash_tabola_bale < seed_data.sql
"""

import argparse
import random
from datetime import datetime, timedelta
from faker import Faker

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate data dummy SQL yang sesuai Milestone2_CRS_The_Dementors_of_Snape.sql"
    )
    parser.add_argument("--klan", type=int, default=30, help="Jumlah data KLAN.")
    parser.add_argument("--akun", type=int, default=150, help="Jumlah data AKUN.")
    parser.add_argument("--seed", type=int, default=42, help="Seed agar hasil reproducible.")
    return parser.parse_args()

args = parse_args()
TOTAL_KLAN = max(1, args.klan)
TOTAL_AKUN = max(5, args.akun)
SEED = args.seed

fake = Faker("id_ID")
Faker.seed(SEED)
fake.seed_instance(SEED)
random.seed(SEED)

def sql_str(value):
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def sql_num_or_null(value):
    return "NULL" if value is None else str(value)

def rand_dt(start_year=2025, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 5, 1)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

lines = []

def emit(text=""):
    lines.append(text)

def emit_insert(table_name, columns, rows, value_formatter, chunk_size=1000):
    if not rows:
        return
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i : i + chunk_size]
        emit(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES")
        values = [f"  ({value_formatter(row)})" for row in chunk]
        emit(",\n".join(values) + ";")
        emit()

MIN_NON_FK_ROWS = 20
MIN_ROWS_PER_FK = 50
MIN_KARTU_ROWS = 100  
MIN_PASUKAN_ROWS = 50
MIN_SIHIR_ROWS = 50
MIN_BANGUNAN_ROWS = 50

BASE_ARENAS = [
    (1, "Training Camp", 0),
    (2, "Goblin Stadium", 300),
    (3, "Bone Pit", 600),
    (4, "Barbarian Bowl", 1000),
    (5, "P.E.K.K.A Playhouse", 1400),
    (6, "Spell Valley", 1700),
    (7, "Builder Workshop", 2000),
    (8, "Royal Arena", 2300),
    (9, "Frozen Peak", 2600),
    (10, "Jungle Arena", 3000),
    (11, "Hog Mountain", 3400),
    (12, "Electro Valley", 3800),
    (13, "Master Arena", 4200),
]
ARENAS = list(BASE_ARENAS)
next_arena_id = len(ARENAS) + 1
next_piala = ARENAS[-1][2] + 300
while len(ARENAS) < MIN_NON_FK_ROWS:
    ARENAS.append((next_arena_id, f"Challenger Arena {next_arena_id}", next_piala))
    next_arena_id += 1
    next_piala += 300

ARENA_BY_PIALA = {arena_id: piala for arena_id, _, piala in ARENAS}

BASE_RARITY_STATS = [
    ("Common", 40, 2, 5),
    ("Rare", 10, 4, 50),
    ("Epic", 4, 10, 400),
    ("Legendary", 1, 20, 20000),
]
RARITY_STATS = list(BASE_RARITY_STATS)
for idx in range(1, MIN_NON_FK_ROWS - len(BASE_RARITY_STATS) + 1):
    RARITY_STATS.append(
        (
            f"Special-{idx}",
            random.randint(1, 40),
            random.randint(2, 30),
            random.randint(10, 50000),
        )
    )
RARITY_MAX_DONASI = {r[0]: r[1] for r in RARITY_STATS}

# (kartu_id, nama, tipe, damage, elixir, rarity, arena_id, deskripsi)
KARTU_BASE = [
    (1, "Knight", "Pasukan", 75, 3, "Common", 1, "Pasukan melee serbaguna."),
    (2, "Archer", "Pasukan", 60, 3, "Common", 1, "Dua pemanah jarak jauh."),
    (3, "Giant", "Pasukan", 120, 5, "Rare", 2, "Tank utama dengan HP besar."),
    (4, "Goblin", "Pasukan", 40, 2, "Common", 1, "Cepat dan murah."),
    (5, "Witch", "Pasukan", 50, 5, "Epic", 5, "Memanggil skeleton berkala."),
    (6, "Baby Dragon", "Pasukan", 80, 4, "Epic", 3, "Serangan area terbang."),
    (7, "Musketeer", "Pasukan", 95, 4, "Rare", 3, "Single target jarak jauh."),
    (8, "PEKKA", "Pasukan", 250, 7, "Epic", 4, "Damage sangat tinggi."),
    (9, "Minions", "Pasukan", 45, 3, "Common", 2, "Pasukan terbang murah."),
    (10, "Balloon", "Pasukan", 300, 5, "Epic", 2, "Target bangunan dari udara."),
    (11, "Valkyrie", "Pasukan", 100, 4, "Rare", 4, "Damage area melee."),
    (12, "Wizard", "Pasukan", 110, 5, "Rare", 5, "Splash damage tinggi."),
    (13, "Mini PEKKA", "Pasukan", 160, 4, "Rare", 3, "Burst damage single."),
    (14, "Skeleton Army", "Pasukan", 35, 3, "Epic", 2, "Kerumunan unit kecil."),
    (15, "Hog Rider", "Pasukan", 130, 4, "Rare", 4, "Serang bangunan cepat."),
    (16, "Mega Minion", "Pasukan", 120, 3, "Rare", 7, "Single target udara."),
    (17, "Dark Prince", "Pasukan", 180, 4, "Epic", 8, "Splash dan charge."),
    (18, "Electro Wizard", "Pasukan", 100, 4, "Legendary", 12, "Stun musuh."),
    (19, "Lumberjack", "Pasukan", 140, 4, "Legendary", 8, "Cepat dan rage drop."),
    (20, "Sparky", "Pasukan", 220, 6, "Legendary", 7, "Damage ledakan besar."),
    (21, "Fireball", "Sihir", 330, 4, "Rare", 1, "Spell area serbaguna."),
    (22, "Lightning", "Sihir", 600, 6, "Epic", 5, "Spell ke 3 target terdekat."),
    (23, "Arrows", "Sihir", 90, 3, "Common", 1, "Spell area murah."),
    (24, "Earthquake", "Sihir", 50, 3, "Rare", 5, "Efektif lawan bangunan."),
    (25, "Rocket", "Sihir", 800, 6, "Rare", 3, "Damage burst besar."),
    (26, "Freeze", "Sihir", 0, 4, "Epic", 4, "Membekukan unit dan bangunan."),
    (27, "Poison", "Sihir", 80, 4, "Epic", 5, "Damage area durasi."),
    (28, "Zap", "Sihir", 100, 2, "Common", 1, "Stun singkat area kecil."),
    (29, "Cannon", "Bangunan", 110, 3, "Common", 1, "Defensive building murah."),
    (30, "Bomb Tower", "Bangunan", 90, 4, "Rare", 2, "Area splash defense."),
    (31, "Inferno Tower", "Bangunan", 100, 5, "Rare", 4, "Melumerkan tank."),
    (32, "Tesla", "Bangunan", 120, 4, "Common", 5, "Bangunan hidden defense."),
    (33, "X-Bow", "Bangunan", 70, 6, "Epic", 6, "Siege building."),
    (34, "Mortar", "Bangunan", 130, 4, "Common", 2, "Long range siege."),
]
KARTU_ROWS = list(KARTU_BASE)
base_rarity_names = [r[0] for r in BASE_RARITY_STATS]
arena_ids = [a[0] for a in ARENAS]
extra_name_pool = [
    "Guardian",
    "Ranger",
    "Crusher",
    "Sentinel",
    "Phantom",
    "Blaster",
    "Lancer",
    "Invoker",
    "Fury",
    "Drifter",
]

def count_by_type(rows, tipe):
    return sum(1 for row in rows if row[2] == tipe)

next_kartu_id = max(k[0] for k in KARTU_ROWS) + 1
while (
    len(KARTU_ROWS) < MIN_KARTU_ROWS
    or count_by_type(KARTU_ROWS, "Pasukan") < MIN_PASUKAN_ROWS
    or count_by_type(KARTU_ROWS, "Sihir") < MIN_SIHIR_ROWS
    or count_by_type(KARTU_ROWS, "Bangunan") < MIN_BANGUNAN_ROWS
):
    if count_by_type(KARTU_ROWS, "Pasukan") < MIN_PASUKAN_ROWS:
        tipe = "Pasukan"
        dmg_min, dmg_max = 45, 260
        elixir_min, elixir_max = 2, 7
    elif count_by_type(KARTU_ROWS, "Sihir") < MIN_SIHIR_ROWS:
        tipe = "Sihir"
        dmg_min, dmg_max = 0, 820
        elixir_min, elixir_max = 2, 7
    elif count_by_type(KARTU_ROWS, "Bangunan") < MIN_BANGUNAN_ROWS:
        tipe = "Bangunan"
        dmg_min, dmg_max = 50, 180
        elixir_min, elixir_max = 3, 7
    else:
        tipe = random.choice(["Pasukan", "Sihir", "Bangunan"])
        dmg_min, dmg_max = 40, 300
        elixir_min, elixir_max = 2, 7

    name_seed = random.choice(extra_name_pool)
    nama = f"{tipe} {name_seed} {next_kartu_id}"
    deskripsi = f"Kartu {tipe.lower()} hasil generate Faker #{next_kartu_id}."
    KARTU_ROWS.append(
        (
            next_kartu_id,
            nama,
            tipe,
            random.randint(dmg_min, dmg_max),
            random.randint(elixir_min, elixir_max),
            random.choice(base_rarity_names),
            random.choice(arena_ids),
            deskripsi,
        )
    )
    next_kartu_id += 1

KARTU_IDS = [k[0] for k in KARTU_ROWS]
KARTU_BY_ID = {k[0]: k for k in KARTU_ROWS}

NEGARA_LIST = [
    "Indonesia",
    "Malaysia",
    "Singapura",
    "Thailand",
    "Vietnam",
    "Filipina",
    "Jepang",
    "Korea Selatan",
    "Tiongkok",
    "India",
    "Australia",
    "Selandia Baru",
    "Amerika Serikat",
    "Kanada",
    "Brasil",
    "Argentina",
    "Meksiko",
    "Kolombia",
    "Inggris",
    "Prancis",
    "Jerman",
    "Belanda",
    "Spanyol",
    "Italia",
    "Polandia",
    "Rusia",
    "Turki",
    "Arab Saudi",
    "Uni Emirat Arab",
    "Mesir",
    "Nigeria",
    "Afrika Selatan",
]
TIPE_KLAN = ["Terbuka", "Hanya Undangan", "Tertutup"]

PESAN_TEMPLATES = [
    "Ada yang mau donasi {kartu} dong?",
    "GG semua! Battle tadi seru banget.",
    "Siapa yang mau push trophy malam ini?",
    "Deck {kartu} recommended buat arena sekarang.",
    "Jangan lupa upgrade kartu sebelum season baru.",
    "Kita lagi butuh anggota aktif, invite teman kalian!",
    "Ada tips buat counter {kartu}?",
    "Season baru mulai besok, siap semua?",
    "Mantap banget tadi menangnya!",
    "Kalian pakai deck apa buat trophy push?",
    "Donasi dulu yuk buat persiapan war.",
    "Selamat bergabung di klan kita!",
    "Ada turnamen internal besok, siap?",
]

def max_arena_for_piala(piala):
    best = 1
    for arena_id, _, piala_min in ARENAS:
        if piala >= piala_min:
            best = arena_id
    return best

# build data
emit("USE clash_tabola_bale;")
emit("SET FOREIGN_KEY_CHECKS = 0;")
emit()

# 1) MASTER TABLES
emit("-- ============================================================")
emit("-- MASTER TABLES")
emit("-- ============================================================")

emit_insert(
    "ARENA",
    ["arena_id", "nama_arena", "piala_dibutuhkan"],
    ARENAS,
    lambda r: f"{r[0]}, {sql_str(r[1])}, {r[2]}",
)

emit_insert(
    "RARITY_STATS",
    ["rarity", "max_terima_donasi", "required_cards", "required_gold"],
    RARITY_STATS,
    lambda r: f"{sql_str(r[0])}, {r[1]}, {r[2]}, {r[3]}",
)

# 2) KLAN
emit("-- ============================================================")
emit(f"-- KLAN ({TOTAL_KLAN} rows)")
emit("-- ============================================================")

klan_rows = []
klan_names_used = set()
for klan_id in range(1, TOTAL_KLAN + 1):
    while True:
        adj = random.choice(
            [
                "Royal",
                "Iron",
                "Golden",
                "Shadow",
                "Thunder",
                "Fire",
                "Storm",
                "Dragon",
                "Phoenix",
                "Crystal",
                "Silver",
                "Dark",
                "Blazing",
                "Frozen",
                "Ancient",
                "Mystic",
                "Swift",
                "Elite",
            ]
        )
        noun = random.choice(
            [
                "Clash",
                "Warriors",
                "Knights",
                "Raiders",
                "Legion",
                "Force",
                "Squad",
                "Army",
                "Guild",
                "Alliance",
                "Brotherhood",
                "Empire",
                "Order",
                "Wolves",
                "Eagles",
                "Tigers",
                "Lions",
            ]
        )
        nama = f"{adj} {noun}"
        if nama not in klan_names_used:
            klan_names_used.add(nama)
            break
        nama = f"{adj} {noun} {klan_id}"
        if nama not in klan_names_used:
            klan_names_used.add(nama)
            break

    klan_rows.append(
        (
            klan_id,
            nama,
            random.choice(NEGARA_LIST),
            random.choice([0, 300, 600, 1000, 1400, 2000, 2600, 3000, 3400]),
            fake.sentence(nb_words=8),
            random.choices(TIPE_KLAN, weights=[60, 30, 10])[0],
        )
    )

emit_insert(
    "KLAN",
    ["klan_id", "nama_klan", "negara_asal_klan", "piala_dibutuhkan", "deskripsi", "tipe_klan"],
    klan_rows,
    lambda r: f"{r[0]}, {sql_str(r[1])}, {sql_str(r[2])}, {r[3]}, {sql_str(r[4])}, {sql_str(r[5])}",
)

# 3) AKUN
emit("-- ============================================================")
emit(f"-- AKUN ({TOTAL_AKUN} rows)")
emit("-- ============================================================")

akun_rows = []
usernames_used = set()
fixed_akuns = [
    (1, "rainaldi", 3200, 1),
    (2, "jonathan_ab", 2800, 1),
    (3, "rafi_akbar", 3800, 1),
    (4, "dika_p", 2300, 1),
    (5, "rinofaros", 3000, 1),
]

for akun_id, username, piala, klan_id in fixed_akuns:
    usernames_used.add(username)
    akun_rows.append(
        {
            "akun_id": akun_id,
            "username": username,
            "kata_sandi": "$2b$10$hashed_fixed",
            "jumlah_emas": random.randint(2000, 10000),
            "jumlah_piala": piala,
            "role": None,
            "waktu_bergabung": rand_dt(2024, 2026),
            "klan_id": klan_id,
        }
    )

for akun_id in range(6, TOTAL_AKUN + 1):
    while True:
        username = f"{fake.user_name()}{random.randint(1, 999)}"
        if username not in usernames_used:
            usernames_used.add(username)
            break

    piala = random.choices(
        [0, 150, 400, 700, 1200, 1800, 2400, 3000, 3600, 4200, 5000],
        weights=[8, 12, 15, 15, 12, 10, 9, 8, 6, 3, 2],
    )[0] + random.randint(0, 299)

    akun_rows.append(
        {
            "akun_id": akun_id,
            "username": username,
            "kata_sandi": "$2b$10$" + fake.md5()[:22],
            "jumlah_emas": random.randint(0, 20000),
            "jumlah_piala": piala,
            "role": None,
            "waktu_bergabung": rand_dt(2024, 2026),
            "klan_id": random.randint(1, TOTAL_KLAN) if random.random() < 0.90 else None,
        }
    )

klan_members = {}
for akun in akun_rows:
    if akun["klan_id"] is not None:
        klan_members.setdefault(akun["klan_id"], []).append(akun)

for members in klan_members.values():
    random.shuffle(members)
    for idx, akun in enumerate(members):
        if idx == 0:
            akun["role"] = "Pemimpin"
        else:
            akun["role"] = random.choices(
                ["Anggota", "Penatua", "Wakil Pemimpin"],
                weights=[78, 14, 8],
            )[0]

emit_insert(
    "AKUN",
    [
        "akun_id",
        "username",
        "kata_sandi",
        "jumlah_emas",
        "jumlah_piala",
        "role",
        "waktu_bergabung",
        "klan_id",
    ],
    akun_rows,
    lambda r: (
        f"{r['akun_id']}, {sql_str(r['username'])}, {sql_str(r['kata_sandi'])}, "
        f"{r['jumlah_emas']}, {r['jumlah_piala']}, {sql_str(r['role'])}, "
        f"{sql_str(r['waktu_bergabung'].strftime('%Y-%m-%d %H:%M:%S'))}, {sql_num_or_null(r['klan_id'])}"
    ),
)

# 4) DECK
emit("-- ============================================================")
emit("-- DECK (1-5 deck per akun)")
emit("-- ============================================================")

deck_rows = []
for akun in akun_rows:
    akun_id = akun["akun_id"]
    total_deck = random.randint(1, 5)
    for nomor_slot in range(1, total_deck + 1):
        deck_rows.append((akun_id, nomor_slot, 1 if nomor_slot == 1 else 0))

emit_insert(
    "DECK",
    ["akun_id", "nomor_slot", "status_aktif"],
    deck_rows,
    lambda r: f"{r[0]}, {r[1]}, {r[2]}",
)

# 5) KARTU + SUBTYPE
emit("-- ============================================================")
emit("-- KARTU + SUBTYPE")
emit("-- ============================================================")

emit_insert(
    "KARTU",
    ["kartu_id", "nama", "deskripsi", "tipe", "damage", "elixir", "rarity", "arena_id"],
    KARTU_ROWS,
    lambda r: (
        f"{r[0]}, {sql_str(r[1])}, {sql_str(r[7])}, {sql_str(r[2])}, "
        f"{r[3]}, {r[4]}, {sql_str(r[5])}, {r[6]}"
    ),
)

pasukan_rows = []
sihir_rows = []
bangunan_rows = []

for kartu in KARTU_ROWS:
    kartu_id, _, tipe, damage, _, _, _, _ = kartu
    if tipe == "Pasukan":
        pasukan_rows.append(
            (
                kartu_id,
                random.randint(300, 2500),
                random.choice(["Darat", "Udara", "Semua"]),
                round(random.uniform(1.0, 6.5), 2),
                random.choice(["Lambat", "Sedang", "Cepat", "Sangat Cepat"]),
                round(random.uniform(0.7, 2.0), 2),
                random.choice(["Melee", "Ranged", "Siege"]),
            )
        )
    elif tipe == "Sihir":
        sihir_rows.append((kartu_id, round(random.uniform(2.0, 5.5), 2)))
    elif tipe == "Bangunan":
        bangunan_rows.append(
            (
                kartu_id,
                random.randint(400, 2500),
                random.choice(["Darat", "Udara", "Semua"]),
                random.randint(25, 70),
                round(random.uniform(3.0, 12.0), 2),
                round(random.uniform(0.8, 2.1), 2),
            )
        )
    else:
        raise ValueError(f"Tipe kartu tidak dikenal: {tipe} (kartu_id={kartu_id}, damage={damage})")

emit_insert(
    "PASUKAN",
    [
        "kartu_id",
        "health",
        "target_serangan",
        "jarak_serangan",
        "kecepatan_gerak",
        "kecepatan_menyerang",
        "tipe_pasukan",
    ],
    pasukan_rows,
    lambda r: f"{r[0]}, {r[1]}, {sql_str(r[2])}, {r[3]}, {sql_str(r[4])}, {r[5]}, {sql_str(r[6])}",
)

emit_insert(
    "SIHIR",
    ["kartu_id", "radius_serangan"],
    sihir_rows,
    lambda r: f"{r[0]}, {r[1]}",
)

emit_insert(
    "BANGUNAN",
    [
        "kartu_id",
        "health",
        "target_serangan",
        "lifetime",
        "jarak_serangan",
        "kecepatan_menyerang",
    ],
    bangunan_rows,
    lambda r: f"{r[0]}, {r[1]}, {sql_str(r[2])}, {r[3]}, {r[4]}, {r[5]}",
)

# 6) KOLEKSI_KARTU
emit("-- ============================================================")
emit("-- KOLEKSI_KARTU")
emit("-- ============================================================")

koleksi_rows = []
akun_koleksi = {}

for akun in akun_rows:
    akun_id = akun["akun_id"]
    piala = akun["jumlah_piala"]
    arena_maks = max_arena_for_piala(piala)
    eligible = [k[0] for k in KARTU_ROWS if k[6] <= arena_maks]

    max_pick = min(24, len(eligible))
    min_pick = min(8, max_pick)
    total_kartu = random.randint(min_pick, max_pick)
    chosen_kartu = random.sample(eligible, total_kartu)
    akun_koleksi[akun_id] = set(chosen_kartu)

    for kartu_id in chosen_kartu:
        level_max = min(14, max(1, 2 + piala // 450))
        level = random.randint(1, level_max)
        jumlah_kartu = random.randint(1, 600)
        koleksi_rows.append((akun_id, kartu_id, level, jumlah_kartu))

emit_insert(
    "KOLEKSI_KARTU",
    ["akun_id", "kartu_id", "level_kartu", "jumlah_kartu"],
    koleksi_rows,
    lambda r: f"{r[0]}, {r[1]}, {r[2]}, {r[3]}",
)

# 7) ISI_DECK
emit("-- ============================================================")
emit("-- ISI_DECK")
emit("-- ============================================================")

isi_deck_rows = []
for akun_id, nomor_slot, _ in deck_rows:
    owned = list(akun_koleksi.get(akun_id, set()))
    if not owned:
        continue
    total_isi = min(8, len(owned))
    for kartu_id in random.sample(owned, total_isi):
        isi_deck_rows.append((akun_id, nomor_slot, kartu_id))

emit_insert(
    "ISI_DECK",
    ["akun_id", "nomor_slot", "kartu_id"],
    isi_deck_rows,
    lambda r: f"{r[0]}, {r[1]}, {r[2]}",
)

# 8) PERTARUNGAN
emit("-- ============================================================")
emit("-- PERTARUNGAN")
emit("-- ============================================================")

arena_members = {}
for akun in akun_rows:
    arena_id = max_arena_for_piala(akun["jumlah_piala"])
    arena_members.setdefault(arena_id, []).append(akun["akun_id"])

pertarungan_rows = []
player_battles = {}
pert_id = 1

for arena_id, members in arena_members.items():
    if len(members) < 2:
        continue
    total_battle = max(10, len(members) * 2)
    for _ in range(total_battle):
        p1, p2 = random.sample(members, 2)
        roll = random.random()
        if roll < 0.45:
            winner = p1
        elif roll < 0.90:
            winner = p2
        else:
            winner = None

        wkt = rand_dt(2025, 2026)
        replay_path = f"/replays/r{pert_id:06d}.mp4"
        pertarungan_rows.append(
            (
                pert_id,
                wkt.year,
                wkt.month,
                wkt.day,
                wkt.hour,
                wkt.minute,
                replay_path,
                p1,
                p2,
                winner,
                arena_id,
            )
        )
        player_battles.setdefault(p1, []).append(pert_id)
        player_battles.setdefault(p2, []).append(pert_id)
        pert_id += 1

emit_insert(
    "PERTARUNGAN",
    [
        "pertarungan_id",
        "tahun",
        "bulan",
        "tanggal",
        "jam",
        "menit",
        "replay_path",
        "akun_pemain_1",
        "akun_pemain_2",
        "id_pemenang",
        "arena_id",
    ],
    pertarungan_rows,
    lambda r: (
        f"{r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]}, {sql_str(r[6])}, "
        f"{r[7]}, {r[8]}, {sql_num_or_null(r[9])}, {r[10]}"
    ),
)

# 9) CHAT + SUBTYPE
emit("-- ============================================================")
emit("-- CHAT + SUBTYPE")
emit("-- ============================================================")

chat_rows = []
pesan_biasa_rows = []
permintaan_donasi_rows = []
berbagi_replay_rows = []

for klan_id in range(1, TOTAL_KLAN + 1):
    members = [akun["akun_id"] for akun in klan_members.get(klan_id, [])]
    if not members:
        continue
    total_chat = random.randint(20, 60)
    urutan_chat = 1

    for _ in range(total_chat):
        sender = random.choice(members)
        wkt = rand_dt(2025, 2026)
        chat_rows.append((klan_id, urutan_chat, wkt.day, wkt.hour, wkt.minute, sender))

        roll = random.random()
        if roll < 0.60:
            kartu_nama = KARTU_BY_ID[random.choice(KARTU_IDS)][1]
            teks = random.choice(PESAN_TEMPLATES).format(kartu=kartu_nama)
            pesan_biasa_rows.append((klan_id, urutan_chat, teks))
        elif roll < 0.85:
            owned = list(akun_koleksi.get(sender, set()))
            if not owned:
                owned = [random.choice(KARTU_IDS)]
            kartu_id = random.choice(owned)
            rarity = KARTU_BY_ID[kartu_id][5]
            jumlah_diterima = random.randint(0, RARITY_MAX_DONASI[rarity])
            permintaan_donasi_rows.append((klan_id, urutan_chat, jumlah_diterima, kartu_id))
        else:
            sender_battles = player_battles.get(sender, [])
            if not sender_battles:
                teks = random.choice(PESAN_TEMPLATES).format(kartu="Knight")
                pesan_biasa_rows.append((klan_id, urutan_chat, teks))
            else:
                pertarungan_id = random.choice(sender_battles)
                deskripsi = random.choice(
                    [
                        "Battle epic banget, wajib tonton!",
                        "Contoh rotasi deck yang bagus.",
                        "Comeback dari ketertinggalan!",
                        "Triple crown pertama gue.",
                        "Perfect defense, bangga banget.",
                        None,
                    ]
                )
                berbagi_replay_rows.append((klan_id, urutan_chat, deskripsi, pertarungan_id))
        urutan_chat += 1

emit_insert(
    "CHAT",
    ["klan_id", "urutan_chat", "tanggal_pengiriman", "jam_pengiriman", "menit_pengiriman", "akun_pengirim_id"],
    chat_rows,
    lambda r: f"{r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]}",
)

emit_insert(
    "PESAN_BIASA",
    ["klan_id", "urutan_chat", "teks_pesan"],
    pesan_biasa_rows,
    lambda r: f"{r[0]}, {r[1]}, {sql_str(r[2])}",
)

emit_insert(
    "PERMINTAAN_DONASI",
    ["klan_id", "urutan_chat", "jumlah_kartu_diterima", "kartu_id"],
    permintaan_donasi_rows,
    lambda r: f"{r[0]}, {r[1]}, {r[2]}, {r[3]}",
)

emit_insert(
    "BERBAGI_REPLAY",
    ["klan_id", "urutan_chat", "deskripsi_tambahan", "pertarungan_id"],
    berbagi_replay_rows,
    lambda r: f"{r[0]}, {r[1]}, {sql_str(r[2])}, {r[3]}",
)

emit("SET FOREIGN_KEY_CHECKS = 1;")
emit()
emit("-- ============================================================")
emit("-- SUMMARY")
emit(f"-- ARENA             : {len(ARENAS)}")
emit(f"-- RARITY_STATS      : {len(RARITY_STATS)}")
emit(f"-- KLAN              : {len(klan_rows)}")
emit(f"-- AKUN              : {len(akun_rows)}")
emit(f"-- DECK              : {len(deck_rows)}")
emit(f"-- KARTU             : {len(KARTU_ROWS)}")
emit(f"-- PASUKAN           : {len(pasukan_rows)}")
emit(f"-- SIHIR             : {len(sihir_rows)}")
emit(f"-- BANGUNAN          : {len(bangunan_rows)}")
emit(f"-- KOLEKSI_KARTU     : {len(koleksi_rows)}")
emit(f"-- ISI_DECK          : {len(isi_deck_rows)}")
emit(f"-- PERTARUNGAN       : {len(pertarungan_rows)}")
emit(f"-- CHAT              : {len(chat_rows)}")
emit(f"-- PESAN_BIASA       : {len(pesan_biasa_rows)}")
emit(f"-- PERMINTAAN_DONASI : {len(permintaan_donasi_rows)}")
emit(f"-- BERBAGI_REPLAY    : {len(berbagi_replay_rows)}")
emit("-- ============================================================")

print("\n".join(lines))