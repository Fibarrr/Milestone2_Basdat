"""
Cara pakai:
    pip install faker
    python seed.py > seed_data.sql
    sudo mysql clash_tabola_bale < seed_data.sql

"""

import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('id_ID')
random.seed(42)

#  helpers 

def sql_str(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def sql_dt(dt):
    return "'" + dt.strftime('%Y-%m-%d %H:%M:%S') + "'"

def rand_dt(start_year=2025, end_year=2026):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 5, 1)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

lines = []
def emit(s=''):
    lines.append(s)

#  static / fixed data 

ARENAS = [
    (1,  'Training Camp',        0),
    (2,  'Goblin Stadium',     300),
    (3,  'Bone Pit',           600),
    (4,  'Barbarian Bowl',    1000),
    (5,  'P.E.K.K.A Playhouse',1400),
    (6,  'Spell Valley',      1700),
    (7,  'Builder Workshop',  2000),
    (8,  'Royal Arena',       2300),
    (9,  'Frozen Peak',       2600),
    (10, 'Jungle Arena',      3000),
    (11, 'Hog Mountain',      3400),
    (12, 'Electro Valley',    3800),
    (13, 'Master Arena',      4200),
]
ARENA_IDS     = [a[0] for a in ARENAS]
ARENA_PIALA   = {a[0]: a[2] for a in ARENAS}

RARITIES = ['Common', 'Rare', 'Epic', 'Legendary']
RARITY_WEIGHT = [50, 30, 15, 5]

KARTU_FIXED = [
    # (id, nama, tipe, damage, elixir, rarity, arena_id)
    (1,  'Knight',          'Pasukan',  75,  3, 'Common',    1),
    (2,  'Archer',          'Pasukan',  60,  3, 'Common',    1),
    (3,  'Giant',           'Pasukan', 120,  5, 'Rare',      2),
    (4,  'Goblin',          'Pasukan',  40,  2, 'Common',    1),
    (5,  'Witch',           'Pasukan',  50,  5, 'Epic',      5),
    (6,  'Baby Dragon',     'Pasukan',  80,  4, 'Epic',      3),
    (7,  'Musketeer',       'Pasukan',  95,  4, 'Rare',      3),
    (8,  'PEKKA',           'Pasukan', 250,  7, 'Epic',      4),
    (9,  'Minions',         'Pasukan',  45,  3, 'Common',    2),
    (10, 'Balloon',         'Pasukan', 300,  5, 'Epic',      2),
    (11, 'Valkyrie',        'Pasukan', 100,  4, 'Rare',      4),
    (12, 'Wizard',          'Pasukan', 110,  5, 'Rare',      5),
    (13, 'Mini PEKKA',      'Pasukan', 160,  4, 'Rare',      3),
    (14, 'Skeleton Army',   'Pasukan',  35,  3, 'Epic',      2),
    (15, 'Hog Rider',       'Pasukan', 130,  4, 'Rare',      4),
    (16, 'Mega Minion',     'Pasukan', 120,  3, 'Rare',      7),
    (17, 'Dark Prince',     'Pasukan', 180,  4, 'Epic',      8),
    (18, 'Electro Wizard',  'Pasukan', 100,  4, 'Legendary', 12),
    (19, 'Lumberjack',      'Pasukan', 140,  4, 'Legendary',  8),
    (20, 'Sparky',          'Pasukan', 220,  6, 'Legendary',  7),
    (21, 'Fireball',        'Sihir',   330,  4, 'Rare',       1),
    (22, 'Lightning',       'Sihir',   600,  6, 'Epic',       5),
    (23, 'Arrows',          'Sihir',    90,  3, 'Common',     1),
    (24, 'Earthquake',      'Sihir',    50,  3, 'Rare',       5),
    (25, 'Rocket',          'Sihir',   800,  6, 'Rare',       3),
    (26, 'Freeze',          'Sihir',     0,  4, 'Epic',       4),
    (27, 'Poison',          'Sihir',    80,  4, 'Epic',       5),
    (28, 'Zap',             'Sihir',   100,  2, 'Common',     1),
    (29, 'Cannon',          'Bangunan',110,  3, 'Common',     1),
    (30, 'Bomb Tower',      'Bangunan', 90,  4, 'Rare',       2),
    (31, 'Inferno Tower',   'Bangunan',100,  5, 'Rare',       4),
    (32, 'Tesla',           'Bangunan',120,  4, 'Common',     5),
    (33, 'X-Bow',           'Bangunan', 70,  6, 'Epic',       6),
    (34, 'Mortar',          'Bangunan',130,  4, 'Common',     2),
]
KARTU_IDS      = [k[0] for k in KARTU_FIXED]
KARTU_ARENA    = {k[0]: k[6] for k in KARTU_FIXED}  # kartu_id -> arena_id yg dibutuhkan


emit("-- ============================================================")
emit("-- KLAN (Test 50 rows)")
emit("-- ============================================================")

NEGARA_LIST = [
    'Indonesia','Malaysia','Singapura','Thailand','Vietnam','Filipina',
    'Jepang','Korea Selatan','Tiongkok','India','Australia','Selandia Baru',
    'Amerika Serikat','Kanada','Brasil','Argentina','Meksiko','Kolombia',
    'Inggris','Prancis','Jerman','Belanda','Spanyol','Italia','Polandia',
    'Rusia','Turki','Arab Saudi','Uni Emirat Arab','Mesir','Nigeria','Afrika Selatan',
]
TIPE_KLAN = ['Terbuka', 'Hanya Undangan', 'Tertutup']

klan_rows = []
klan_names_used = set()
for i in range(1, 51):
    while True:
        adj  = random.choice(['Royal','Iron','Golden','Shadow','Thunder','Fire',
                               'Storm','Dragon','Phoenix','Crystal','Silver','Dark',
                               'Blazing','Frozen','Ancient','Mystic','Swift','Elite'])
        noun = random.choice(['Clash','Warriors','Knights','Raiders','Legion','Force',
                               'Squad','Army','Guild','Alliance','Brotherhood','Clan',
                               'Empire','Order','Wolves','Eagles','Tigers','Lions'])
        nama = f"{adj} {noun}"
        if nama not in klan_names_used:
            klan_names_used.add(nama)
            break
    negara      = random.choice(NEGARA_LIST)
    piala_min   = random.choice([0, 0, 300, 600, 1000, 1400, 2000, 2600, 3000])
    deskripsi   = fake.sentence(nb_words=8)
    tipe        = random.choices(TIPE_KLAN, weights=[60, 30, 10])[0]
    jumlah_ang  = random.randint(1, 50)
    klan_rows.append((i, nama, negara, piala_min, deskripsi, tipe, jumlah_ang))

emit("INSERT INTO Klan (klan_id, nama_klan, negara_asal_klan, piala_minimal, deskripsi, tipe_klan, jumlah_anggota) VALUES")
vals = []
for r in klan_rows:
    vals.append(f"  ({r[0]}, {sql_str(r[1])}, {sql_str(r[2])}, {r[3]}, {sql_str(r[4])}, {sql_str(r[5])}, {r[6]})")
emit(",\n".join(vals) + ";")
emit()

# 3. AKUN (300 akun) 

emit("-- ============================================================")
emit("-- AKUN (Test 300 rows)")
emit("-- ============================================================")

akun_rows = []
usernames_used = set()
# Pastikan anggota kelompok ada
fixed_akuns = [
    (1,  'rainaldi',    3200, 1),
    (2,  'jonathan_ab', 2800, 1),
    (3,  'rafi_akbar',  3800, 1),
    (4,  'dika_p',      2300, 1),
    (5,  'rinofaros',   3000, 1),
]
for fid, uname, piala, klan in fixed_akuns:
    usernames_used.add(uname)
    emas = piala * random.randint(1, 3)
    akun_rows.append((fid, uname, '$2b$10$hashed_fixed', emas, piala, klan))

for i in range(6, 301):
    while True:
        uname = fake.user_name() + str(random.randint(1, 999))
        if uname not in usernames_used:
            usernames_used.add(uname)
            break
    piala   = random.choices(
        [0, 150, 400, 700, 1200, 1800, 2400, 3000, 3600, 4200, 5000],
        weights=[10, 15, 15, 15, 10, 10, 8, 7, 5, 3, 2]
    )[0] + random.randint(0, 299)
    emas    = random.randint(0, 15000)
    klan_id = random.randint(1, 50) if random.random() < 0.85 else None
    pw      = '$2b$10$' + fake.md5()[:22]
    akun_rows.append((i, uname, pw, emas, piala, klan_id))

emit("INSERT INTO Akun (akun_id, username, kata_sandi, jumlah_emas, jumlah_piala, klan_id) VALUES")
vals = []
for r in akun_rows:
    klan_val = str(r[5]) if r[5] is not None else 'NULL'
    vals.append(f"  ({r[0]}, {sql_str(r[1])}, {sql_str(r[2])}, {r[3]}, {r[4]}, {klan_val})")
emit(",\n".join(vals) + ";")
emit()

#  4. ANGGOTA 

emit("-- ============================================================")
emit("-- ANGGOTA")
emit("-- ============================================================")

# Kumpulkan akun per klan
klan_members = {}  # klan_id -> [akun_id]
for r in akun_rows:
    if r[5] is not None:
        klan_members.setdefault(r[5], []).append(r[0])

ROLES = ['Anggota', 'Penatua', 'Wakil Pemimpin', 'Pemimpin']
ROLE_W = [70, 15, 10, 5]

anggota_rows = []
for klan_id, members in klan_members.items():
    # Pastikan minimal ada 1 Pemimpin
    has_leader = False
    for idx, akun_id in enumerate(members):
        if not has_leader and idx == len(members) - 1:
            role = 'Pemimpin'
        else:
            role = random.choices(ROLES, weights=ROLE_W)[0]
            if role == 'Pemimpin':
                if has_leader:
                    role = 'Penatua'
                else:
                    has_leader = True
        wbergabung = rand_dt(2024, 2026)
        anggota_rows.append((akun_id, klan_id, role, wbergabung))

emit("INSERT INTO Anggota (akun_id, klan_id, role, waktu_bergabung) VALUES")
vals = []
for r in anggota_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {sql_str(r[2])}, {sql_dt(r[3])})")
emit(",\n".join(vals) + ";")
emit()

#  5. DECK 

emit("-- ============================================================")
emit("-- DECK (1-5 deck per akun)")
emit("-- ============================================================")

deck_rows = []
akun_deck_count = {}  # akun_id -> jumlah deck
for r in akun_rows:
    akun_id   = r[0]
    n_decks   = random.randint(1, 5)
    akun_deck_count[akun_id] = n_decks
    for slot in range(1, n_decks + 1):
        status = (slot == 1)  # slot 1 selalu aktif
        deck_rows.append((slot, akun_id, status))

emit("INSERT INTO Deck (nomor_slot, akun_id, status_aktif) VALUES")
vals = []
for r in deck_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {1 if r[2] else 0})")
emit(",\n".join(vals) + ";")
emit()

#  6. KOLEKSI 

emit("-- ============================================================")
emit("-- KOLEKSI (akun - kartu)")
emit("-- ============================================================")

koleksi_rows = []
akun_koleksi = {}  # akun_id -> set(kartu_id)

def max_arena_for_piala(piala):
    best = 1
    for aid, pmin in ARENA_PIALA.items():
        if piala >= pmin:
            best = aid
    return best

for r in akun_rows:
    akun_id   = r[0]
    piala     = r[4]
    max_arena = max_arena_for_piala(piala)
    # Kartu yang boleh dimiliki: arena_id <= max_arena
    eligible  = [k[0] for k in KARTU_FIXED if k[6] <= max_arena]
    n_kartu   = min(len(eligible), random.randint(4, min(20, len(eligible))))
    chosen    = random.sample(eligible, n_kartu)
    akun_koleksi[akun_id] = set(chosen)
    for kartu_id in chosen:
        level = random.randint(1, min(14, 3 + piala // 500))
        jumlah = random.randint(1, 300)
        koleksi_rows.append((akun_id, kartu_id, level, jumlah))

emit("INSERT INTO Koleksi (akun_id, kartu_id, level_kartu, jumlah_kartu) VALUES")
vals = []
for r in koleksi_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {r[2]}, {r[3]})")
emit(",\n".join(vals) + ";")
emit()

#  7. BERISI 

emit("-- ============================================================")
emit("-- BERISI (deck - kartu, maks 8 unik per deck)")
emit("-- ============================================================")

berisi_rows = []
for nomor_slot, akun_id, _ in deck_rows:
    owned = list(akun_koleksi.get(akun_id, set()))
    if len(owned) < 1:
        continue
    n = min(8, len(owned))
    chosen = random.sample(owned, n)
    for kartu_id in chosen:
        berisi_rows.append((nomor_slot, akun_id, kartu_id))

emit("INSERT INTO Berisi (nomor_slot, akun_id, kartu_id) VALUES")
vals = []
for r in berisi_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {r[2]})")
emit(",\n".join(vals) + ";")
emit()

# 8. PERTARUNGAN (200+ rows) 

emit("-- ============================================================")
emit("-- PERTARUNGAN (200+ rows)")
emit("-- ============================================================")

# Group akun by arena mereka
arena_akun = {}  # arena_id -> [akun_id]
for r in akun_rows:
    akun_id = r[0]
    piala   = r[4]
    arena   = max_arena_for_piala(piala)
    arena_akun.setdefault(arena, []).append(akun_id)

pert_rows = []
pert_id = 1
for arena_id, members in arena_akun.items():
    if len(members) < 2:
        continue
    # jumlah pertarungan proporsional
    n_battles = max(4, len(members) * 2)
    for _ in range(n_battles):
        p1, p2 = random.sample(members, 2)
        roll = random.random()
        if roll < 0.45:
            winner = p1
        elif roll < 0.90:
            winner = p2
        else:
            winner = None  # seri
        wtime = rand_dt(2025, 2026)
        replay = f'/replays/r{pert_id:04d}.mp4'
        pert_rows.append((pert_id, wtime, replay, arena_id, p1, p2, winner))
        pert_id += 1

emit("INSERT INTO Pertarungan (pertarungan_id, waktu_pertarungan, replay_path, arena_id, akun_id_player1, akun_id_player2, akun_id_pemenang) VALUES")
vals = []
for r in pert_rows:
    winner_val = str(r[6]) if r[6] is not None else 'NULL'
    vals.append(f"  ({r[0]}, {sql_dt(r[1])}, {sql_str(r[2])}, {r[3]}, {r[4]}, {r[5]}, {winner_val})")
emit(",\n".join(vals) + ";")
emit()

# 9. CHAT + SUB-TYPE 

emit("-- ============================================================")
emit("-- CHAT + sub-types (Pesan_Biasa, Permintaan_Donasi, Berbagi_Replay)")
emit("-- ============================================================")

PESAN_TEMPLATES = [
    "Ada yang mau donasi {} dong?",
    "GG semua! Battle tadi seru banget.",
    "Siapa yang mau war malam ini?",
    "Deck {} recommended buat arena sekarang.",
    "Jangan lupa upgrade kartu sebelum season baru.",
    "Kita lagi butuh anggota aktif, invite teman kalian!",
    "Ada yang punya tips buat countering {}?",
    "Season baru mulai besok, siap semua?",
    "Mantap banget tadi menangnya!",
    "Kalian pakai deck apa buat trophy push?",
    "Donasi dulu yuk buat persiapan war.",
    "Selamat bergabung di klan kita!",
    "Ada tournament besok, siap?",
    "Tips: {} bagus banget buat counter deck control.",
    "Jangan lupa claim daily reward ya.",
]

chat_rows      = []
pesan_rows     = []
donasi_rows    = []
replay_rows    = []

# Buat pert_ids lookup: arena -> [pert_id]
arena_pert = {}
for r in pert_rows:
    arena_pert.setdefault(r[3], []).append(r[0])

for klan_id, members in klan_members.items():
    if not members:
        continue
    n_chat = random.randint(10, 40)
    urutan = 1
    used_pert_in_klan = set()

    for _ in range(n_chat):
        sender = random.choice(members)
        wtime  = rand_dt(2025, 2026)
        chat_rows.append((urutan, klan_id, sender, wtime))

        # Tentukan sub-type (disjoint)
        roll = random.random()
        if roll < 0.60:
            # Pesan Biasa
            kartu_name = random.choice(KARTU_FIXED)[1]
            teks = random.choice(PESAN_TEMPLATES).format(kartu_name)
            pesan_rows.append((urutan, klan_id, teks))
        elif roll < 0.85:
            # Permintaan Donasi
            # Pilih kartu yang dimiliki sender
            owned = list(akun_koleksi.get(sender, set()))
            if not owned:
                owned = [random.choice(KARTU_IDS)]
            kartu_id = random.choice(owned)
            max_don  = {'Common': 10, 'Rare': 5, 'Epic': 1, 'Legendary': 1}
            rarity   = next(k[5] for k in KARTU_FIXED if k[0] == kartu_id)
            diterima = random.randint(0, max_don[rarity])
            donasi_rows.append((urutan, klan_id, kartu_id, diterima))
        else:
            # Berbagi Replay — butuh pertarungan yang melibatkan sender
            sender_pert = [r[0] for r in pert_rows if r[4] == sender or r[5] == sender]
            if not sender_pert:
                # fallback ke Pesan Biasa
                teks = random.choice(PESAN_TEMPLATES).format('Knight')
                pesan_rows.append((urutan, klan_id, teks))
            else:
                pid = random.choice(sender_pert)
                desc = random.choice([
                    'Battle epic banget, wajib tonton!',
                    'Contoh deck yang bagus nih.',
                    'Comeback dari ketertinggalan!',
                    'Triple crown pertama gue.',
                    'Perfect defense, bangga banget.',
                    None
                ])
                replay_rows.append((urutan, klan_id, pid, desc))
        urutan += 1

emit("INSERT INTO Chat (urutan_chat, klan_id, akun_id, waktu_pengiriman) VALUES")
vals = []
for r in chat_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {r[2]}, {sql_dt(r[3])})")
emit(",\n".join(vals) + ";")
emit()

emit("INSERT INTO Pesan_Biasa (urutan_chat, klan_id, teks_pesan) VALUES")
vals = []
for r in pesan_rows:
    vals.append(f"  ({r[0]}, {r[1]}, {sql_str(r[2])})")
emit(",\n".join(vals) + ";")
emit()

if donasi_rows:
    emit("INSERT INTO Permintaan_Donasi (urutan_chat, klan_id, kartu_id, jumlah_kartu_diterima) VALUES")
    vals = []
    for r in donasi_rows:
        vals.append(f"  ({r[0]}, {r[1]}, {r[2]}, {r[3]})")
    emit(",\n".join(vals) + ";")
    emit()

if replay_rows:
    emit("INSERT INTO Berbagi_Replay (urutan_chat, klan_id, pertarungan_id, deskripsi_tambahan) VALUES")
    vals = []
    for r in replay_rows:
        vals.append(f"  ({r[0]}, {r[1]}, {r[2]}, {sql_str(r[3])})")
    emit(",\n".join(vals) + ";")
    emit()

#  FOOTER 

emit("SET FOREIGN_KEY_CHECKS = 1;")
emit()
emit("-- ============================================================")
emit("-- Summary perkiraan row count:")
emit(f"-- Klan        : {len(klan_rows)}")
emit(f"-- Akun        : {len(akun_rows)}")
emit(f"-- Anggota     : {len(anggota_rows)}")
emit(f"-- Deck        : {len(deck_rows)}")
emit(f"-- Koleksi     : {len(koleksi_rows)}")
emit(f"-- Berisi      : {len(berisi_rows)}")
emit(f"-- Pertarungan : {len(pert_rows)}")
emit(f"-- Chat        : {len(chat_rows)}")
emit(f"-- Pesan_Biasa : {len(pesan_rows)}")
emit(f"-- Permintaan  : {len(donasi_rows)}")
emit(f"-- Berbagi_Rep : {len(replay_rows)}")
emit("-- ============================================================")

#  OUTPUT 
print("\n".join(lines))