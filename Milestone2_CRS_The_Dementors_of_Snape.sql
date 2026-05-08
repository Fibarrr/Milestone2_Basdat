

SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS clash_tabola_bale;
CREATE DATABASE clash_tabola_bale
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE clash_tabola_bale;
SET FOREIGN_KEY_CHECKS = 1;

-- TABEL INDEPENDEN 

CREATE TABLE Arena (
    arena_id    INT             NOT NULL AUTO_INCREMENT,
    nama_arena  VARCHAR(100)    NOT NULL,
    piala_dibutuhkan INT        NOT NULL DEFAULT 0,
    PRIMARY KEY (arena_id)
);

CREATE TABLE Rarity_stats (
    rarity              VARCHAR(50)     NOT NULL,
    max_terima_donasi   INT             NOT NULL,
    required_cards      INT             NOT NULL,
    required_gold       INT             NOT NULL,
    PRIMARY KEY (rarity)
);

CREATE TABLE Klan (
    klan_id         INT             NOT NULL AUTO_INCREMENT,
    nama_klan       VARCHAR(100)    NOT NULL,
    negara_asal_klan VARCHAR(100)   NOT NULL,
    piala_minimal   INT             NOT NULL DEFAULT 0,
    deskripsi       TEXT,
    tipe_klan       ENUM('Terbuka','Hanya Undangan','Tertutup') NOT NULL DEFAULT 'Terbuka',
    jumlah_anggota  INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (klan_id)
);

CREATE TABLE Kartu (
    kartu_id    INT             NOT NULL AUTO_INCREMENT,
    nama        VARCHAR(100)    NOT NULL,
    deskripsi   TEXT,
    tipe        ENUM('Pasukan','Sihir','Bangunan') NOT NULL,
    damage      INT             NOT NULL DEFAULT 0,
    elixir      INT             NOT NULL CHECK (elixir BETWEEN 1 AND 10),
    rarity      VARCHAR(50)     NOT NULL,
    arena_id    INT             NOT NULL,
    PRIMARY KEY (kartu_id),
    CONSTRAINT fk_kartu_rarity  FOREIGN KEY (rarity)   REFERENCES Rarity_stats(rarity),
    CONSTRAINT fk_kartu_arena   FOREIGN KEY (arena_id)  REFERENCES Arena(arena_id)
);

-- Sub-type Pasukan (disjoint ISA dari Kartu)
CREATE TABLE Pasukan (
    kartu_id            INT             NOT NULL,
    health_pasukan      INT             NOT NULL,
    target_serangan     ENUM('Udara','Darat','Semua') NOT NULL DEFAULT 'Semua',
    jarak_serangan      DECIMAL(5,2)    NOT NULL,
    kecepatan_gerak     DECIMAL(5,2)    NOT NULL,
    kecepatan_menyerang DECIMAL(5,2)    NOT NULL,
    tipe_pasukan        ENUM('Udara','Darat') NOT NULL,
    PRIMARY KEY (kartu_id),
    CONSTRAINT fk_pasukan_kartu FOREIGN KEY (kartu_id) REFERENCES Kartu(kartu_id) ON DELETE CASCADE
);

-- Sub-type Sihir (disjoint ISA dari Kartu)
CREATE TABLE Sihir (
    kartu_id            INT             NOT NULL,
    radius_serangan     DECIMAL(5,2)    NOT NULL,
    PRIMARY KEY (kartu_id),
    CONSTRAINT fk_sihir_kartu   FOREIGN KEY (kartu_id) REFERENCES Kartu(kartu_id) ON DELETE CASCADE
);

-- Sub-type Bangunan (disjoint ISA dari Kartu)
CREATE TABLE Bangunan (
    kartu_id            INT             NOT NULL,
    health_bangunan     INT             NOT NULL,
    target_serangan     ENUM('Udara','Darat','Semua') NOT NULL DEFAULT 'Semua',
    lifetime            INT             NOT NULL COMMENT 'dalam detik',
    jarak_serangan      DECIMAL(5,2)    NOT NULL,
    kecepatan_menyerang DECIMAL(5,2)    NOT NULL,
    PRIMARY KEY (kartu_id),
    CONSTRAINT fk_bangunan_kartu FOREIGN KEY (kartu_id) REFERENCES Kartu(kartu_id) ON DELETE CASCADE
);


-- TABEL AKUN

CREATE TABLE Akun (
    akun_id         INT             NOT NULL AUTO_INCREMENT,
    username        VARCHAR(100)    NOT NULL UNIQUE,
    kata_sandi      VARCHAR(255)    NOT NULL,
    jumlah_emas     INT             NOT NULL DEFAULT 0,
    jumlah_piala    INT             NOT NULL DEFAULT 0,
    klan_id         INT             NULL COMMENT 'NULL jika belum bergabung klan',
    role            ENUM('Anggota','Penatua','Wakil Pemimpin','Pemimpin') DEFAULT 'Anggota',
    waktu_bergabung DATETIME        NULL,
    PRIMARY KEY (akun_id),
    CONSTRAINT fk_akun_klan FOREIGN KEY (klan_id) REFERENCES Klan(klan_id) ON DELETE SET NULL
);

-- Relasi Anggota (Akun-Klan) — atribut role dan waktu_bergabung



-- TABEL DECK (Weak Entity — bergantung pada Akun)

CREATE TABLE Deck (
    nomor_slot      INT             NOT NULL CHECK (nomor_slot BETWEEN 1 AND 5),
    akun_id         INT             NOT NULL,
    status_aktif    BOOLEAN         NOT NULL DEFAULT FALSE,
    PRIMARY KEY (nomor_slot, akun_id),
    CONSTRAINT fk_deck_akun FOREIGN KEY (akun_id) REFERENCES Akun(akun_id) ON DELETE CASCADE
);


-- RELASI KOLEKSI (Akun - Kartu) M:N

CREATE TABLE Koleksi (
    akun_id         INT             NOT NULL,
    kartu_id        INT             NOT NULL,
    level_kartu     INT             NOT NULL DEFAULT 1,
    jumlah_kartu    INT             NOT NULL DEFAULT 1,
    PRIMARY KEY (akun_id, kartu_id),
    CONSTRAINT fk_koleksi_akun  FOREIGN KEY (akun_id)  REFERENCES Akun(akun_id)  ON DELETE CASCADE,
    CONSTRAINT fk_koleksi_kartu FOREIGN KEY (kartu_id) REFERENCES Kartu(kartu_id) ON DELETE CASCADE
);

-- RELASI BERISI (Deck - Kartu) M:N

CREATE TABLE Berisi (
    nomor_slot      INT             NOT NULL,
    akun_id         INT             NOT NULL,
    kartu_id        INT             NOT NULL,
    PRIMARY KEY (nomor_slot, akun_id, kartu_id),
    CONSTRAINT fk_berisi_deck   FOREIGN KEY (nomor_slot, akun_id) REFERENCES Deck(nomor_slot, akun_id) ON DELETE CASCADE,
    CONSTRAINT fk_berisi_kartu  FOREIGN KEY (kartu_id)            REFERENCES Kartu(kartu_id)           ON DELETE CASCADE
);


-- TABEL PERTARUNGAN (N-ary: Player1, Player2, Pemenang, Arena)
-- arena_id langsung disini

CREATE TABLE Pertarungan (
    pertarungan_id      INT             NOT NULL AUTO_INCREMENT,
    waktu_pertarungan   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    replay_path         VARCHAR(500)    NULL,
    arena_id            INT             NOT NULL,
    akun_id_player1     INT             NOT NULL,
    akun_id_player2     INT             NOT NULL,
    deck_slot_player1   INT             NOT NULL COMMENT 'Slot deck akun 1',
    deck_slot_player2   INT             NOT NULL COMMENT 'Slot deck akun 2',
    akun_id_pemenang    INT             NULL COMMENT 'NULL jika seri',
    PRIMARY KEY (pertarungan_id),
    CONSTRAINT fk_pert_arena    FOREIGN KEY (arena_id)          REFERENCES Arena(arena_id),
    CONSTRAINT fk_pert_p1       FOREIGN KEY (akun_id_player1)   REFERENCES Akun(akun_id),
    CONSTRAINT fk_pert_p2       FOREIGN KEY (akun_id_player2)   REFERENCES Akun(akun_id),
    CONSTRAINT fk_pert_winner   FOREIGN KEY (akun_id_pemenang)  REFERENCES Akun(akun_id)
);


-- TABEL CHAT (Weak Entity — agregat Anggota/Akun-Klan)
-- terhubung ke agregat Akun-Klan (akun_id + klan_id)

CREATE TABLE Chat (
    urutan_chat     INT             NOT NULL,
    klan_id         INT             NOT NULL,
    akun_id         INT             NOT NULL,
    waktu_pengiriman DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (urutan_chat, klan_id),
    CONSTRAINT fk_chat_klan     FOREIGN KEY (klan_id)           REFERENCES Klan(klan_id)  ON DELETE CASCADE,
    -- Sekarang merujuk langsung ke Akun karena data role & klan sudah ada di sana
    CONSTRAINT fk_chat_akun     FOREIGN KEY (akun_id)           REFERENCES Akun(akun_id) ON DELETE CASCADE
);

-- Sub-type Pesan Biasa (disjoint ISA dari Chat)
CREATE TABLE Pesan_Biasa (
    urutan_chat     INT             NOT NULL,
    klan_id         INT             NOT NULL,
    teks_pesan      TEXT            NOT NULL,
    PRIMARY KEY (urutan_chat, klan_id),
    CONSTRAINT fk_pb_chat FOREIGN KEY (urutan_chat, klan_id) REFERENCES Chat(urutan_chat, klan_id) ON DELETE CASCADE
);

-- Sub-type Permintaan Donasi (disjoint ISA dari Chat)
CREATE TABLE Permintaan_Donasi (
    urutan_chat         INT             NOT NULL,
    klan_id             INT             NOT NULL,
    kartu_id            INT             NOT NULL COMMENT 'Kartu yang diminta',
    jumlah_kartu_diterima INT           NOT NULL DEFAULT 0,
    PRIMARY KEY (urutan_chat, klan_id),
    CONSTRAINT fk_pd_chat   FOREIGN KEY (urutan_chat, klan_id) REFERENCES Chat(urutan_chat, klan_id) ON DELETE CASCADE,
    CONSTRAINT fk_pd_kartu  FOREIGN KEY (kartu_id)             REFERENCES Kartu(kartu_id)
);

-- Sub-type Berbagi Replay (disjoint ISA dari Chat)
-- Total participation ke Pertarungan (NOT NULL)
CREATE TABLE Berbagi_Replay (
    urutan_chat         INT             NOT NULL,
    klan_id             INT             NOT NULL,
    pertarungan_id      INT             NOT NULL COMMENT 'Total participation — wajib ada',
    deskripsi_tambahan  TEXT            NULL,
    PRIMARY KEY (urutan_chat, klan_id),
    CONSTRAINT fk_br_chat   FOREIGN KEY (urutan_chat, klan_id) REFERENCES Chat(urutan_chat, klan_id) ON DELETE CASCADE,
    CONSTRAINT fk_br_pert   FOREIGN KEY (pertarungan_id)       REFERENCES Pertarungan(pertarungan_id)
);



-- VIEWS


CREATE OR REPLACE VIEW v_akun_arena AS
SELECT a.akun_id, a.username, a.jumlah_piala,
       ar.arena_id, ar.nama_arena
FROM Akun a
JOIN Arena ar ON a.jumlah_piala >= ar.piala_dibutuhkan
WHERE ar.arena_id = (
    SELECT MAX(ar2.arena_id)
    FROM Arena ar2
    WHERE a.jumlah_piala >= ar2.piala_dibutuhkan
);

-- data di-seed via seed.py / seed_data.sql
