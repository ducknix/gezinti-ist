#!/usr/bin/env bash
# coding: utf-8

echo -e "\e[1;37m\nGezinti.ist Paketleyici\n\e[0m"

files='setup.py src/gezinti.py src/views/api.pyx src/views/geo.pyx src/views/index.pyx src/views/user.pyx'
ico_ok='[\e[1;32m+\e[0m]'
ico_no='[\e[1;31m-\e[0m]'
ico_pr="[\e[1;34m*\e[0m]"

# ================== Dosya Kontrolleri ================== #
echo -e "$ico_pr Dosya kontrolleri yapılıyor."
if [[ ! -d "src" ]]; then
    echo -e "$ico_no src dizini bulunamadı. \n\nÇıkılyor .."
    exit 1
fi
for file in $files; do
    if [[ -f "$file" ]]; then
        echo -e "$ico_ok $file bulundu."
    else
        echo -e "$ico_no $file bulunamadı. \n\nÇıkılıyor..\n"
        exit 1
    fi
done
# ======================================================= #

# Cythonize

# ==================

# dist oluşturma ve paketleme

# ==================

# final
