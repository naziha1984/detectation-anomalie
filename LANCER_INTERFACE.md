# 🚀 Guide de Lancement de l'Interface

## ⚠️ Problèmes Courants et Solutions

### Problème 1: "streamlit n'est pas reconnu"

**Solution:** Utilisez `python -m streamlit` au lieu de `streamlit`

```powershell
python -m streamlit run app.py
```

### Problème 2: "run_app.bat n'est pas reconnu"

**Solution:** Dans PowerShell, utilisez `.\run_app.bat` avec le point et le slash

```powershell
.\run_app.bat
```

## ✅ Méthodes de Lancement (Windows PowerShell)

### Méthode 1: Commande Directe (Recommandée)
```powershell
python -m streamlit run app.py
```

### Méthode 2: Script Batch
```powershell
.\run_app.bat
```

### Méthode 3: Avec Port Personnalisé
```powershell
python -m streamlit run app.py --server.port 8501
```

## 🌐 Accès à l'Interface

Une fois lancée, l'interface sera accessible à:
- **URL locale:** http://localhost:8501
- **URL réseau:** http://VOTRE_IP:8501

## 🔍 Vérification de l'Installation

Vérifiez que Streamlit est bien installé:
```powershell
python -m pip show streamlit
```

Si ce n'est pas installé:
```powershell
python -m pip install streamlit plotly
```

## 📝 Commandes Utiles

### Arrêter l'application
Appuyez sur `Ctrl+C` dans le terminal

### Voir les options disponibles
```powershell
python -m streamlit run app.py --help
```

### Mode sans navigateur automatique
```powershell
python -m streamlit run app.py --server.headless true
```

## 🆘 Dépannage

### Erreur: "No module named streamlit"
```powershell
python -m pip install streamlit plotly
```

### Erreur: "Port already in use"
Changez le port:
```powershell
python -m streamlit run app.py --server.port 8502
```

### L'interface ne s'ouvre pas automatiquement
Ouvrez manuellement votre navigateur et allez sur:
http://localhost:8501

