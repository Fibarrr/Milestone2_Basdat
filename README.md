# Milestone2_Basdat

cara run:

 1. Generate seed data
python seed.py > seed_data.sql

 2. Import schema (DDL)
mysql -u root -p < Milestone2_CRS_The_Dementors_of_Snape.sql

 3. Import data
mysql -u root -p < seed_data.sql

4. Buka Mariadb (kalau tidak automatis)
mysql -u root -p

5. Pilih

USE clash_tabola_bale;

###

Apabila melakukan perubahan dan ingin run ulang:

 1. Drop database lama
mysql -u root -p -e "DROP DATABASE clash_tabola_bale;"

 2. Generate seed baru (kalau ada perubahan di seed.py)
python seed.py > seed_data.sql

 3. Import schema
mysql -u root -p < Milestone2_CRS_The_Dementors.sql

 4. Import data
mysql -u root -p < seed_data.sql

5. Buka Mariadb (kalau tidak automatis)
mysql -u root -p


######

File Milestone + Seed

mysql -u root -p < Milestone2_CRS_TheDementorsOfSnape.sql

mysql -u root -p -e "USE clash_tabola_bale; SHOW TABLES;"

mysql -u root -p

USE clash_tabola_bale;