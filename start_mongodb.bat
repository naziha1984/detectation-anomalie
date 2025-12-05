@echo off
echo ========================================
echo    E-COMMERCE IA - MONGODB VERSION
echo ========================================
echo.

echo Initialisation de la base de donnees MongoDB...
python init_mongodb.py

echo.
echo Demarrage de l'application avec MongoDB...
echo L'application sera accessible sur: http://localhost:5000
echo.
echo Comptes de test disponibles:
echo - admin / admin123 (administrateur)
echo - kenza_douiri / password123
echo - fatima_gatt / password123
echo - naziha_jr / password123
echo - oubey_boubakri / password123
echo - med_ali / password123
echo.

python app_mongodb.py

pause
