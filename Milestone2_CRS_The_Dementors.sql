SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS clash_tabola_bale;
CREATE DATABASE clash_tabola_bale
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE clash_tabola_bale;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. TABEL MASTER (Dibuat paling awal karena tidak punya Foreign Key)
CREATE TABLE ARENA (
    arena_id INT PRIMARY KEY,
    nama_arena VARCHAR(50) NOT NULL,
    piala_dibutuhkan INT NOT NULL
);

CREATE TABLE RARITY_STATS (
    rarity VARCHAR(20) PRIMARY KEY,
    max_terima_donasi INT NOT NULL,
    required_cards INT NOT NULL,
    required_gold INT NOT NULL
);

CREATE TABLE KLAN (
    klan_id INT PRIMARY KEY,
    nama_klan VARCHAR(50) NOT NULL,
    negara_asal_klan VARCHAR(50),
    piala_dibutuhkan INT NOT NULL,
    deskripsi TEXT,
    tipe_klan VARCHAR(20)
);

-- 2. TABEL ENTITAS INTI
CREATE TABLE AKUN (
    akun_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    kata_sandi VARCHAR(255) NOT NULL,
    jumlah_emas INT DEFAULT 0,
    jumlah_piala INT DEFAULT 0,
    role VARCHAR(20),
    waktu_bergabung DATETIME,
    klan_id INT,
    FOREIGN KEY (klan_id) REFERENCES KLAN(klan_id) ON DELETE SET NULL
);

-- DECK (Weak Entity milik Akun) -> ON DELETE CASCADE
CREATE TABLE DECK (
    akun_id INT,
    nomor_slot INT,
    status_aktif BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (akun_id, nomor_slot),
    FOREIGN KEY (akun_id) REFERENCES AKUN(akun_id) ON DELETE CASCADE
);

CREATE TABLE KARTU (
    kartu_id INT PRIMARY KEY,
    nama VARCHAR(50) NOT NULL,
    deskripsi TEXT,
    tipe VARCHAR(20) NOT NULL,
    damage INT,
    elixir INT NOT NULL,
    rarity VARCHAR(20),
    arena_id INT,
    FOREIGN KEY (rarity) REFERENCES RARITY_STATS(rarity),
    FOREIGN KEY (arena_id) REFERENCES ARENA(arena_id)
);

-- 3. TABEL SUB-TYPE KARTU
CREATE TABLE PASUKAN (
    kartu_id INT PRIMARY KEY,
    health INT,
    target_serangan VARCHAR(30),
    jarak_serangan DECIMAL(5,2),
    kecepatan_gerak VARCHAR(20),
    kecepatan_menyerang DECIMAL(5,2),
    tipe_pasukan VARCHAR(30),
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

CREATE TABLE SIHIR (
    kartu_id INT PRIMARY KEY,
    radius_serangan DECIMAL(5,2),
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

CREATE TABLE BANGUNAN (
    kartu_id INT PRIMARY KEY,
    health INT,
    target_serangan VARCHAR(30),
    lifetime INT,
    jarak_serangan DECIMAL(5,2),
    kecepatan_menyerang DECIMAL(5,2),
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

-- 4. TABEL PERSIMPANGAN (M:N & TRANSAKSI)
CREATE TABLE KOLEKSI_KARTU (
    akun_id INT,
    kartu_id INT,
    level_kartu INT DEFAULT 1,
    jumlah_kartu INT DEFAULT 0,
    PRIMARY KEY (akun_id, kartu_id),
    FOREIGN KEY (akun_id) REFERENCES AKUN(akun_id) ON DELETE CASCADE,
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

CREATE TABLE ISI_DECK (
    akun_id INT,
    nomor_slot INT,
    kartu_id INT,
    PRIMARY KEY (akun_id, nomor_slot, kartu_id),
    FOREIGN KEY (akun_id, nomor_slot) REFERENCES DECK(akun_id, nomor_slot) ON DELETE CASCADE,
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

-- Revisi Partisipasi Pertarungan di Arena
CREATE TABLE PERTARUNGAN (
    pertarungan_id INT PRIMARY KEY,
    tahun INT NOT NULL,
    bulan INT NOT NULL,
    tanggal INT NOT NULL,
    jam INT NOT NULL,
    menit INT NOT NULL,
    replay_path VARCHAR(255),
    akun_pemain_1 INT NOT NULL,
    akun_pemain_2 INT NOT NULL,
    id_pemenang INT,
    arena_id INT NOT NULL,
    FOREIGN KEY (akun_pemain_1) REFERENCES AKUN(akun_id),
    FOREIGN KEY (akun_pemain_2) REFERENCES AKUN(akun_id),
    FOREIGN KEY (id_pemenang) REFERENCES AKUN(akun_id),
    FOREIGN KEY (arena_id) REFERENCES ARENA(arena_id)
);

-- 5. TABEL CHAT (Agregasi) & SUB-TYPENYA
CREATE TABLE CHAT (
    klan_id INT,
    urutan_chat INT,
    tanggal_pengiriman INT,
    jam_pengiriman INT,
    menit_pengiriman INT,
    akun_pengirim_id INT NOT NULL,
    PRIMARY KEY (klan_id, urutan_chat),
    FOREIGN KEY (klan_id) REFERENCES KLAN(klan_id) ON DELETE CASCADE,
    FOREIGN KEY (akun_pengirim_id) REFERENCES AKUN(akun_id) ON DELETE CASCADE
);

CREATE TABLE PESAN_BIASA (
    klan_id INT,
    urutan_chat INT,
    teks_pesan TEXT NOT NULL,
    PRIMARY KEY (klan_id, urutan_chat),
    FOREIGN KEY (klan_id, urutan_chat) REFERENCES CHAT(klan_id, urutan_chat) ON DELETE CASCADE
);

CREATE TABLE PERMINTAAN_DONASI (
    klan_id INT,
    urutan_chat INT,
    jumlah_kartu_diterima INT DEFAULT 0,
    kartu_id INT NOT NULL,
    PRIMARY KEY (klan_id, urutan_chat),
    FOREIGN KEY (klan_id, urutan_chat) REFERENCES CHAT(klan_id, urutan_chat) ON DELETE CASCADE,
    FOREIGN KEY (kartu_id) REFERENCES KARTU(kartu_id) ON DELETE CASCADE
);

CREATE TABLE BERBAGI_REPLAY (
    klan_id INT,
    urutan_chat INT,
    deskripsi_tambahan TEXT,
    pertarungan_id INT NOT NULL,
    PRIMARY KEY (klan_id, urutan_chat),
    FOREIGN KEY (klan_id, urutan_chat) REFERENCES CHAT(klan_id, urutan_chat) ON DELETE CASCADE,
    FOREIGN KEY (pertarungan_id) REFERENCES PERTARUNGAN(pertarungan_id) ON DELETE CASCADE
);
